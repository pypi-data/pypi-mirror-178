import logging
import math
import typing

import fameio.source.validator as fameio
from PySide2 import QtCore
from fameio.source.schema import AttributeSpecs

from famegui import models
from famegui.agent_controller import AgentController
from famegui.appworkingdir import AppWorkingDir
from famegui.models import Agent, Contract


class ProjectProperties(QtCore.QObject):
    """Class used to attach extra properties to a scenario model and signal when they change"""

    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self, file_path=""):
        self._has_unsaved_changes = False
        self._file_path = file_path
        self._validation_errors = []
        self.changed.emit()

    @property
    def has_unsaved_changes(self) -> bool:
        return self._has_unsaved_changes

    def set_unsaved_changes(self, has_changes: bool = True):
        if self._has_unsaved_changes != has_changes:
            self._has_unsaved_changes = has_changes
            self.changed.emit()

    @property
    def file_path(self) -> str:
        return self._file_path

    def set_file_path(self, file_path: str) -> None:
        if self._file_path != file_path:
            self._file_path = file_path
            self.changed.emit()

    @property
    def is_validation_successful(self) -> bool:
        return len(self._validation_errors) == 0

    @property
    def validation_errors(self) -> typing.List[str]:
        return self._validation_errors

    def clear_validation_errors(self) -> None:
        was_invalid = not self.is_validation_successful
        self._validation_errors = []
        if was_invalid:
            logging.info("schema validation status changed to valid")
            self.changed.emit()

    def set_validation_error(self, msg: str) -> None:
        assert msg != ""
        was_valid = self.is_validation_successful
        self._validation_errors = [msg]
        if was_valid:
            logging.info("schema validation status changed to invalid")
            self.changed.emit()


class MainController(QtCore.QObject):
    # agent selection update
    selected_agent_changed = QtCore.Signal(AgentController)
    # new agent added
    agent_added = QtCore.Signal(AgentController)
    # new contract added
    contract_added = QtCore.Signal(AgentController, AgentController, models.Contract)  # sender, receiver, contract
    layout_rearranged = QtCore.Signal()

    class AgentTypeBucket:
        def __init__(self, type_name: str, agent: Agent = None, agent_list=None):
            self.type_name = type_name
            self.agent_list = [agent]
            if agent_list is not None:
                self.agent_list = agent_list

        type_name: str
        degree_per_agent: float
        radius_scale_factor_per_agent_type: float
        agent_list: typing.List[Agent]

    def __init__(self, working_dir: AppWorkingDir):
        super().__init__()
        logging.debug("initializing main controller")
        self._working_dir = working_dir
        self._scenario_model = None
        self._agents = {}
        self._contracts = {}
        self._project_properties = ProjectProperties()

    def reset(self, scenario: models.Scenario = None) -> None:
        self._agents = {}
        self._contracts = {}
        self._scenario_model = scenario
        self._project_properties.reset()

    @property
    def is_open(self) -> bool:
        return self._scenario_model is not None

    @property
    def has_unsaved_changes(self) -> bool:
        return self.project_properties.has_unsaved_changes

    @property
    def project_properties(self) -> ProjectProperties:
        return self._project_properties

    @property
    def schema(self) -> models.Schema:
        return self.scenario.schema

    @property
    def scenario(self) -> models.Scenario:
        return self._scenario_model

    def update_scenario_properties(self, props: models.GeneralProperties):
        has_changed = self._scenario_model.update_properties(props)
        if has_changed:
            self._project_properties.set_unsaved_changes(True)

    @property
    def can_export_protobuf(self) -> bool:
        return self.is_open and self.project_properties.is_validation_successful and not self.has_unsaved_changes

    @property
    def agent_count(self) -> int:
        return len(self._agents)

    @property
    def agent_list(self) -> typing.List[AgentController]:
        return self._agents.values()

    def agent_from_id(self, id: int) -> AgentController:
        assert id in self._agents
        return self._agents[id]

    @property
    def contract_count(self) -> int:
        return len(self._contracts)

    def _get_agent_bucket_list(self, agent_list: list) -> list:
        agent_type_bucket_list = []

        for agent in agent_list:

            for x in agent_type_bucket_list:
                if x.type_name == agent.type_name:
                    x.agent_list.append(agent)
                    break
            else:
                agent_type_bucket_list.append(self.AgentTypeBucket(agent.type_name, agent))
        return agent_type_bucket_list

    def prepare_and_sort_agent_buckets(self, agent_type_bucket_list):
        new_agents_list = []
        for item in agent_type_bucket_list:
            new_agents_list.append(item.agent_list)
        new_agents_list.sort(key=len)
        return new_agents_list

    def _split_agent_types_into_chunks(self, agent_type_bucket_list):
        agent_types_to_re_gen_list = []
        chunked_list = []
        # split huge agent bucket into separate to make canvas look better

        # if len(item.agent_list) > 360:
        # create more bucket to make more smaller circles

        for item in agent_type_bucket_list:
            if len(item.agent_list) > 360:
                agent_types_to_re_gen_list.append(item.type_name)

                for i in range(0, len(item.agent_list), 360):
                    chunked_list.append(item.agent_list[i : i + 360])
        return agent_types_to_re_gen_list, chunked_list

    def _calc_degree_per_agent_in_agent_circle(self, agent_type_bucket_list):
        for item in agent_type_bucket_list:
            item.degree_per_agent = 360 / len(item.agent_list)

    def _update_graph_items(self, agent_ctrl_list, new_agent_x, new_agent_y, agent):
        for agent_ctrl in agent_ctrl_list:
            if agent.id.__eq__(agent_ctrl.id):
                agent_ctrl.scene_item.setPos(new_agent_x, new_agent_y)
                agent_ctrl.model_was_modified.emit()
                agent_ctrl.position_changed()
                break

    def auto_scale_scenario_graph(self, agent_ctrl_list: [AgentController], rearrange_mode=False):

        try:
            # sort for better view
            agent_list: list = self._scenario_model.agents

            agent_type_bucket_list = self._get_agent_bucket_list(agent_list)

            # combine buckets (lists)

            new_list = []

            for item in self.prepare_and_sort_agent_buckets(agent_type_bucket_list):
                for x in item:
                    new_list.append(x)
            agent_types_to_re_gen_list, chunked_list = self._split_agent_types_into_chunks(agent_type_bucket_list)

            last_list = []
            for type_to_rm in agent_types_to_re_gen_list:
                agent_type_bucket_list = [value for value in agent_type_bucket_list if value.type_name != type_to_rm]

            for sub_list in chunked_list:
                agent_type_bucket_list.append(self.AgentTypeBucket(sub_list[0].type_name, agent_list=sub_list))

            self._calc_degree_per_agent_in_agent_circle(agent_type_bucket_list)

            agent_type_bucket_list = sorted(agent_type_bucket_list, key=lambda x: len(x.agent_list))

            default_radius = 100.0
            radius = 50
            margin = 20
            last_x = 0.0
            last_y = 0.0

            min_distance = (float(radius) * 2) + float(margin)

            for item in agent_type_bucket_list:
                # expand rad for new circle
                new_radius = default_radius * 1.1

                if new_radius - default_radius < min_distance:
                    new_radius = new_radius + radius * 2 + margin
                default_radius = new_radius

                for i in range(0, len(item.agent_list)):

                    agent = item.agent_list[i]
                    degree = item.degree_per_agent

                    for counter in range(0, i):
                        degree = degree + item.degree_per_agent

                    new_agent_x = default_radius * math.cos(math.radians(degree))
                    new_agent_y = default_radius * math.sin(math.radians(degree))
                    distance = math.sqrt((new_agent_x - last_x) ** 2 + (new_agent_y - last_y) ** 2)
                    temp_rad: float = default_radius

                    if last_x != 0.0 and last_y != 0.0:
                        # adjust till all spacing requirements are met
                        while distance <= (radius * 2):
                            temp_rad = temp_rad * 1.1
                            new_agent_x = temp_rad * math.cos(math.radians(degree))
                            new_agent_y = temp_rad * math.sin(math.radians(degree))
                            distance = math.sqrt((new_agent_x - last_x) ** 2 + (new_agent_y - last_y) ** 2)
                    default_radius = temp_rad

                    last_x = new_agent_x
                    last_y = new_agent_y

                    if not rearrange_mode:
                        agent.set_display_xy(int(new_agent_x), int(new_agent_y))
                        last_list.append(agent)
                        continue

                    self._update_graph_items(agent_ctrl_list, new_agent_x, new_agent_y, agent)

            if not rearrange_mode:
                for a in last_list:
                    self._create_agent_controller(a)
                for c in self._scenario_model.contracts:
                    self._create_contract_model(c)

        except Exception as e:
            logging.error("failed to init the given scenario: {}".format(e))
            self.reset()
            raise

        # refresh the UI
        self._project_properties.changed.emit()

        # self._controller.reset()

    def compute_scene_rect(self) -> QtCore.QRectF:
        rect = QtCore.QRectF(0, 0, 10000, 10000)

        if len(self.agent_list) >= 5000:
            rect = QtCore.QRectF(0, 0, 100000, 100000)

        for a in self.agent_list:
            margin = 20
            item_size = a.scene_item.boundingRect().width()
            left = a.scene_item.x() - margin
            right = a.scene_item.x() + item_size + margin
            top = a.scene_item.y() + -margin
            bottom = a.scene_item.y() + item_size + margin
            if left < rect.left():
                rect.setLeft(left)
            if right > rect.right():
                rect.setRight(right)
            if top < rect.top():
                rect.setTop(top)
            if bottom > rect.bottom():
                rect.setBottom(bottom)

        return rect

    def get_contract(self, sender_id, receiver_id, product_name) -> Contract:
        for i in self.scenario.contracts:
            i: Contract
            if i.product_name.__eq__(product_name):
                if i.sender_id.__eq__(sender_id) and i.receiver_id.__eq__(receiver_id):
                    return i

                elif i.sender_id.__eq__(receiver_id) and i.receiver_id.__eq__(sender_id):
                    return i

    def get_help_text_for_attr(self, agent_name: str, attr_name: str) -> str:
        for name, spec in self.schema.agent_type_from_name(agent_name).attributes.items():
            spec: AttributeSpecs
            if name.__eq__(attr_name):
                return spec.help_text

    # self.schema.agent_types

    def generate_new_agent_id(self):
        new_id = len(self._agents) + 1
        # note: we don't control how ids have been generated for agents created from an external source
        # so we check for possible conflict and solve it
        if new_id in self._agents:
            for i in range(1, len(self._agents) + 2):
                if i not in self._agents:
                    new_id = i
                    break
        logging.debug("generated new agent id {}".format(new_id))
        return new_id

    # the given agent id can be 0 to clear the current selection
    def set_selected_agent_id(self, agent_id: int):
        assert self.is_open
        if agent_id not in self._agents:
            assert agent_id == 0 or agent_id is None
            self.selected_agent_changed.emit(None)
        else:
            self.selected_agent_changed.emit(self._agents[agent_id])

    def add_new_agent(self, agent_model: models.Agent, x: int, y: int):
        assert self.is_open
        agent_model.set_display_xy(x, y)
        self._create_agent_controller(agent_model)

        self._scenario_model.add_agent(agent_model)
        self._project_properties.set_unsaved_changes(True)
        self.revalidate_scenario()
        logging.info("created new agent {} of type '{}'".format(agent_model.display_id, agent_model.type_name))

    def _create_agent_controller(self, agent_model: models.Agent):
        assert self.is_open

        # accept to add the agent even if invalid
        agent_ctrl = AgentController(agent_model)
        self._agents[agent_ctrl.id] = agent_ctrl
        agent_ctrl.model_was_modified.connect(self._project_properties.set_unsaved_changes)

        logging.info("new agent {} added".format(agent_ctrl.display_id))
        self.agent_added.emit(agent_ctrl)

    def add_new_contract(self, contract_model: models.Contract):
        self._scenario_model.add_contract(contract_model)
        self._create_contract_model(contract_model)
        self._project_properties.set_unsaved_changes(True)
        self.revalidate_scenario()
        logging.info(
            "created new contract '{}' between {} and {}".format(
                contract_model.product_name,
                contract_model.display_sender_id,
                contract_model.display_receiver_id,
            )
        )

    def _create_contract_model(self, contract: models.Contract):
        assert self.is_open

        # validate sender / receiver are known
        if contract.sender_id not in self._agents:
            raise ValueError(
                "can't add contract '{}' because sender agent id '{}' is unknown".format(
                    contract.product_name, contract.sender_id
                )
            )

        if contract.receiver_id not in self._agents:
            raise ValueError(
                "can't add contract '{}' because receiver agent id '{}' is unknown".format(
                    contract.product_name, contract.receiver_id
                )
            )

        sender_ctrl = self._agents[contract.sender_id]
        receiver_ctrl = self._agents[contract.receiver_id]

        # connect agents
        sender_ctrl.model.add_output(contract.receiver_id)
        receiver_ctrl.model.add_input(contract.sender_id)

        self.contract_added.emit(sender_ctrl, receiver_ctrl, contract)

    def rearrange_layout(self):
        self.auto_scale_scenario_graph(self.agent_list, True)

    def revalidate_scenario(self):
        assert self._scenario_model is not None
        try:
            fameio.SchemaValidator.ensure_is_valid_scenario(self._scenario_model)
            self._project_properties.clear_validation_errors()
        except fameio.ValidationException as e:
            err_msg = str(e)
            logging.warning("failed to validate the scenario: {}".format(err_msg))
            self._project_properties.set_validation_error(err_msg)

    def init_scenario_model(self, scenario: models.Scenario, file_path: str):
        logging.debug("opening new scenario")
        rearrange_mode = False

        if self.is_open:
            rearrange_mode = True

        self.reset()

        try:
            self._scenario_model = scenario
            self._project_properties.reset(file_path)
            self._project_properties.set_unsaved_changes(True)

            if not rearrange_mode:
                # process and validate the scenario
                for a in self._scenario_model.agents:
                    self._create_agent_controller(a)
                for c in self._scenario_model.contracts:
                    self._create_contract_model(c)

                self.revalidate_scenario()
                return

            agent_ctrl_list = self._agents

            try:
                # sort for better view
                agent_list: list = self._scenario_model.agents

                agent_type_bucket_list = []

                for agent in agent_list:

                    for x in agent_type_bucket_list:
                        if x.type_name == agent.type_name:
                            x.agent_list.append(agent)
                            break
                    else:
                        agent_type_bucket_list.append(self.AgentTypeBucket(agent.type_name, agent))

                # split huge agent bucket into separate to make canvas look better

                # if len(item.agent_list) > 360:

                # combine buckets (lists)
                new_agents_list = []
                for item in agent_type_bucket_list:
                    new_agents_list.append(item.agent_list)
                new_list = []
                new_agents_list.sort(key=len)

                for item in new_agents_list:
                    for x in item:
                        new_list.append(x)

                # create more bucket to make more smaller circles
                agent_types_to_re_gen_list = []
                chunked_list = []

                for item in agent_type_bucket_list:
                    if len(item.agent_list) > 360:
                        agent_types_to_re_gen_list.append(item.type_name)

                        for i in range(0, len(item.agent_list), 360):
                            chunked_list.append(item.agent_list[i : i + 360])

                last_list = []
                for type_to_rm in agent_types_to_re_gen_list:
                    agent_type_bucket_list = [
                        value for value in agent_type_bucket_list if value.type_name != type_to_rm
                    ]

                for sub_list in chunked_list:
                    agent_type_bucket_list.append(self.AgentTypeBucket(sub_list[0].type_name, agent_list=sub_list))

                for item in agent_type_bucket_list:
                    item.degree_per_agent = 360 / len(item.agent_list)
                agent_type_bucket_list = sorted(agent_type_bucket_list, key=lambda x: len(x.agent_list))

                default_radius = 100.0
                radius = 50
                margin = 20

                last_x = 0.0
                last_y = 0.0

                min_distance = (float(radius) * 2) + float(margin)

                for item in agent_type_bucket_list:
                    # expand rad for new circle
                    new_radius = default_radius * 1.1
                    # TODO make sure agents don't overlap and make sure circles are not to far away

                    if new_radius - default_radius < min_distance:
                        new_radius = new_radius + radius * 2 + margin
                    default_radius = new_radius

                    circle_extent = default_radius * math.pi * 2

                    for i in range(0, len(item.agent_list)):

                        agent = item.agent_list[i]
                        degree = item.degree_per_agent

                        for counter in range(0, i):
                            degree = degree + item.degree_per_agent

                        new_agent_x = default_radius * math.cos(math.radians(degree))
                        new_agent_y = default_radius * math.sin(math.radians(degree))
                        distance = math.sqrt((new_agent_x - last_x) ** 2 + (new_agent_y - last_y) ** 2)

                        distance = math.sqrt((new_agent_x - last_x) ** 2 + (new_agent_y - last_y) ** 2)
                        temp_rad: float = default_radius

                        if last_x != 0.0 and last_y != 0.0:
                            while distance <= (radius * 2):
                                temp_rad = temp_rad * 1.1
                                new_agent_x = temp_rad * math.cos(math.radians(degree))
                                new_agent_y = temp_rad * math.sin(math.radians(degree))
                                distance = math.sqrt((new_agent_x - last_x) ** 2 + (new_agent_y - last_y) ** 2)
                        default_radius = temp_rad

                        last_x = new_agent_x
                        last_y = new_agent_y

                        if not rearrange_mode:
                            agent.set_display_xy(int(new_agent_x), int(new_agent_y))
                            last_list.append(agent)
                            continue

                        for agent_ctrl in agent_ctrl_list:
                            if agent.id.__eq__(agent_ctrl.id):
                                agent_ctrl.scene_item.setPos(new_agent_x, new_agent_y)
                                agent_ctrl.model_was_modified.emit()
                                agent_ctrl.position_changed()
                                break

                if not rearrange_mode:
                    for a in last_list:
                        self._create_agent_controller(a)
                    for c in self._scenario_model.contracts:
                        self._create_contract_model(c)

            except Exception as e:
                logging.error("failed to init the given scenario: {}".format(e))
                self.reset()
                raise

            # refresh the UI
            self._project_properties.changed.emit()

            self.revalidate_scenario()
        except Exception as e:
            logging.error("failed to init the given scenario: {}".format(e))
            self.reset()
            raise

        # refresh the UI

        self._project_properties.changed.emit()

        self.revalidate_scenario()

    def save_to_file(self, file_path):
        assert self.is_open
        models.ScenarioLoader.save_to_yaml_file(self._scenario_model, file_path)
        # update status
        self._project_properties.set_unsaved_changes(False)
        self._project_properties.set_file_path(file_path)
        self.revalidate_scenario()
