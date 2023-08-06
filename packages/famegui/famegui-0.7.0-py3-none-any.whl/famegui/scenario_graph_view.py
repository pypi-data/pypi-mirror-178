import PySide2
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QEvent
from PySide2.QtGui import QFocusEvent, Qt
from PySide2.QtWidgets import QGraphicsSceneMouseEvent
from typing import List

from famegui.scenario_graph_view_items import AgentGraphItem, ContractGraphItem
from famegui.agent_controller import AgentController


class ScenarioGraphView(QtWidgets.QGraphicsScene):
    """View responsible of displaying the scenario as a graph"""

    # (x, y)
    agent_creation_requested = QtCore.Signal(int, int)
    # (agent_id)
    agent_edition_requested = QtCore.Signal(int)
    # (sender_id, receiver_id)
    contract_creation_requested = QtCore.Signal(int, int)
    # agent_id (can be None)
    selected_agent_changed = QtCore.Signal(int)
    # zoom factor control
    zoom_in_requested = QtCore.Signal()

    # multi selection
    released_multi_selection_mode = QtCore.Signal(list, list)
    released_multi_selection_mode_no_valid = QtCore.Signal()

    zoom_out_requested = QtCore.Signal()

    def __init__(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.selectionChanged.connect(self._on_scene_selection_changed)
        self._selected_source_agents = []
        self._selected_target_agents = []
        self._is_in_multi_selection_mode = False
        self.last_state_alt_pressed = False

    def is_in_multi_selection_mode(self) -> bool:
        return self._is_in_multi_selection_mode

    def set_multi_selection_mode(self, in_selection_mode: bool):
        self._is_in_multi_selection_mode = in_selection_mode

    def clearSelection(self, clear_highlights=False) -> None:
        if clear_highlights:
            for agent in self.get_agent_items():
                agent.set_border_highlight(False)
                agent.setSelected(False)

        super().clearSelection()

    @property
    def selected_agent_id(self):
        items = self.selectedItems()
        if len(items) == 1:
            item = items[0]
            assert item.type() == AgentGraphItem.Type
            return item.agent_id
        return None

    def get_contract_items(self) -> List[ContractGraphItem]:
        return_list = []
        for item in self.items():
            if issubclass(type(item), ContractGraphItem):
                return_list.append(item)
        return return_list

    def get_agent_items(self) -> List[AgentGraphItem]:
        return_list = []
        for item in self.items():
            if issubclass(type(item), AgentGraphItem):
                return_list.append(item)
        return return_list

    def add_agent(self, agent_ctrl: AgentController):
        # create item
        item = AgentGraphItem(agent_ctrl.id, agent_ctrl.type_name, agent_ctrl.svg_color)
        item.setToolTip(agent_ctrl.tooltip_text)
        item.setPos(agent_ctrl.x, agent_ctrl.y)
        item.setZValue(100.0)
        # add item
        self.addItem(item)
        agent_ctrl.set_scene_item(item)

    def add_contract(self, sender: AgentController, receiver: AgentController):
        self.addItem(ContractGraphItem(sender.scene_item, receiver.scene_item))

    def event(self, event: PySide2.QtCore.QEvent) -> bool:
        # Enter Multi Selection Mode
        if issubclass(type(event), QGraphicsSceneMouseEvent):
            event: QGraphicsSceneMouseEvent
            if event.modifiers() == QtCore.Qt.ShiftModifier:
                self.set_multi_selection_mode(True)
                click_pos = event.scenePos()
                if event.button() == QtCore.Qt.LeftButton:
                    for item in self.items(click_pos):
                        if item.type() == AgentGraphItem.Type:
                            item: AgentGraphItem
                            item.setSelected(True)
                            if not self._selected_source_agents.__contains__(item):
                                self._selected_source_agents.append(item)

                if event.button() == QtCore.Qt.RightButton:
                    for item in self.items(click_pos):
                        if item.type() == AgentGraphItem.Type:
                            item: AgentGraphItem
                            item.setSelected(True, False)

                            if not self._selected_target_agents.__contains__(item):
                                self._selected_target_agents.append(item)

        return super().event(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        click_pos = event.scenePos()
        # is the double click on an agent item?
        for item in self.items(click_pos):
            if item.type() == AgentGraphItem.Type:
                self.agent_edition_requested.emit(item.agent_id)
                return

        self.agent_creation_requested.emit(click_pos.x(), click_pos.y())

    def keyReleaseEvent(self, event: PySide2.QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Shift:
            self.set_multi_selection_mode(False)
            # EXIT MULTI SELECTION MODE
            if len(self._selected_source_agents) != 0 and len(self._selected_target_agents) != 0:
                self.released_multi_selection_mode.emit(
                    [x.agent_id for x in self._selected_target_agents],
                    [x.agent_id
                     for x in self._selected_source_agents])
                self._selected_target_agents.clear()
                self._selected_source_agents.clear()
                for item in self.get_contract_items():
                    item.setSelected(False)
                super().keyReleaseEvent(event)
                return
            self._selected_target_agents.clear()
            self._selected_source_agents.clear()
            self.released_multi_selection_mode_no_valid.emit()

        super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        # Multi SELECT MODE

        if event.button() == QtCore.Qt.RightButton and event.modifiers() != QtCore.Qt.ShiftModifier:
            click_pos = event.scenePos()
            for item in self.items(click_pos):
                if item.type() == AgentGraphItem.Type:
                    self._on_agent_right_clicked(item.agent_id)
                    return

        QtWidgets.QGraphicsScene.mousePressEvent(self, event)

    def wheelEvent(self, event):
        # enable zoom in/out if ctrl key is pressed
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if event.delta() > 0:
                self.zoom_in_requested.emit()
            else:
                self.zoom_out_requested.emit()

            event.accept()

    def _on_agent_right_clicked(self, agent_id):
        source_id = self.selected_agent_id
        if source_id is not None and source_id != agent_id:
            self.contract_creation_requested.emit(source_id, agent_id)

    def _on_scene_selection_changed(self):
        self.selected_agent_changed.emit(self.selected_agent_id)
