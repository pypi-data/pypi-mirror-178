from PySide2.QtWidgets import QDialog, QDialogButtonBox, QLineEdit
from PySide2 import QtCore, QtGui, QtWidgets
from typing import List

from .generated.ui_dialog_newcontract import Ui_DialogNewContract

from famegui import models
from famegui.agent_controller import AgentController
from .time_utils import convert_gui_datetime_to_fame_time, convert_datetime_to_fame, convert_fame_time_to_gui_datetime


class DialogNewContract(QDialog):
    fame_to_datetime_conversion_triggered: bool = False

    def _configure_line_edit_for_unsigned_int(self, line_edit: QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegExp("\\d{1,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def _configure_line_edit_for_signed_int(self, line_edit: QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegExp("-?\\d{1,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def _configure_line_edit_for_optional_signed_int(self, line_edit: QLineEdit):
        line_edit.setText("")
        line_edit.setPlaceholderText(self.tr("optional"))
        regex_uint64 = QtCore.QRegExp("-?\\d{0,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))

    def __init__(
            self,
            sender: AgentController,
            receiver: AgentController,
            schema: models.Schema,
            parent=None,
    ):
        QDialog.__init__(self, parent)
        self._ui = Ui_DialogNewContract()
        self._ui.setupUi(self)
        self._sender = sender
        self._receiver = receiver

        self.setWindowTitle(self.tr("New contract"))
        self._ui.labelDescr.setText(
            self.tr(
                "<html><head/><body>"
                "<p>Create new contract between:</p>"
                "<ul>"
                "<li>Sender: agent <b>{}</b> of type <b>{}</b></li>"
                "<li>Receiver: agent <b>{}</b> of type <b>{}</b></li>"
                "</ul>"
                "</body></html>"
            ).format(
                sender.display_id,
                sender.type_name,
                receiver.display_id,
                receiver.type_name,
            )
        )
        # accept uint64 numbers as specified in protobuf schema
        self._configure_line_edit_for_unsigned_int(self._ui.lineDeliveryInterval)
        self._configure_line_edit_for_signed_int(self._ui.lineFirstDeliveryTime)
        self._configure_line_edit_for_optional_signed_int(self._ui.lineExpirationTime)

        # fill possible products to select based on the sender schema agent type
        sender_type = schema.agent_type_from_name(sender.type_name)
        assert sender_type is not None
        self._ui.comboBoxProduct.addItems(sender_type.products)

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(self._update_ok_button_status)
        self._update_ok_button_status()

        self._ui.lineFirstDeliveryNonFameTime.setCalendarPopup(True)
        self._ui.lineFirstDeliveryNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineFirstDeliveryNonFameTime.dateTimeChanged.connect(self._update_fame_times)
        self._ui.lineExpirationTimeNonFameTime.setCalendarPopup(True)
        self._ui.lineExpirationTimeNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineExpirationTimeNonFameTime.dateTimeChanged.connect(self._update_fame_times)

        self._ui.lineFirstDeliveryTime.textChanged.connect(self._update_fame_time_text_areas)
        self._ui.lineExpirationTime.textChanged.connect(self._update_fame_time_text_areas)

        # accept uint64 numbers as specified in protobuf schema
        self._configure_line_edit_for_unsigned_int(self._ui.lineDeliveryInterval)
        self._configure_line_edit_for_signed_int(self._ui.lineFirstDeliveryTime)
        self._configure_line_edit_for_optional_signed_int(self._ui.lineExpirationTime)

        # fill possible products to select based on the sender schema agent type
        sender_type = schema.agent_type_from_name(sender.type_name)
        assert sender_type is not None
        self._ui.comboBoxProduct.addItems(sender_type.products)

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(self._update_ok_button_status)
        self._update_ok_button_status()

        self._ui.lineFirstDeliveryNonFameTime.setCalendarPopup(True)
        self._ui.lineFirstDeliveryNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineFirstDeliveryNonFameTime.dateTimeChanged.connect(self._update_fame_times)
        self._ui.lineExpirationTimeNonFameTime.setCalendarPopup(True)
        self._ui.lineExpirationTimeNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineExpirationTimeNonFameTime.dateTimeChanged.connect(self._update_fame_times)

        self._ui.lineFirstDeliveryTime.textChanged.connect(self._update_fame_time_text_areas)
        self._ui.lineExpirationTime.textChanged.connect(self._update_fame_time_text_areas)

    def make_new_contract(self) -> models.Contract:
        expiration_time_str = self._ui.lineExpirationTime.text()
        expiration_time = int(expiration_time_str) if expiration_time_str else None

        return models.Contract(
            self._sender.id,
            self._receiver.id,
            self._ui.comboBoxProduct.currentText(),
            int(self._ui.lineDeliveryInterval.text()),
            int(self._ui.lineFirstDeliveryTime.text()),
            expiration_time,
        )

    def _update_fame_time_text_areas(self):
        self.fame_to_datetime_conversion_triggered = True

        fame_first_delivery_time: str = self._ui.lineFirstDeliveryTime.text()
        if fame_first_delivery_time == "":
            return
        gui_start_time = convert_fame_time_to_gui_datetime(int(fame_first_delivery_time))
        self._ui.lineFirstDeliveryNonFameTime.setDateTime(gui_start_time)

        fame_expiration_time: str = self._ui.lineExpirationTime.text()
        if fame_expiration_time == "":
            return

        gui_expiration_time_time = convert_fame_time_to_gui_datetime(int(fame_expiration_time))
        self._ui.lineExpirationTimeNonFameTime.setDateTime(gui_expiration_time_time)

    def _update_fame_times(self):
        if self.fame_to_datetime_conversion_triggered:
            self.fame_to_datetime_conversion_triggered = False
            return
        self._ui.lineExpirationTime.setText(
            str(convert_gui_datetime_to_fame_time(self._ui.lineExpirationTimeNonFameTime.text()))
        )
        self._ui.lineFirstDeliveryTime.setText(
            str(convert_gui_datetime_to_fame_time(self._ui.lineFirstDeliveryNonFameTime.text()))
        )

    def _update_ok_button_status(self):
        all_fields_ok = (
                self._ui.comboBoxProduct.currentText() != ""
                and self._ui.lineDeliveryInterval.text() != ""
                and self._ui.lineFirstDeliveryTime.text() != ""
        )
        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(all_fields_ok)


class DialogNewMultiContract(DialogNewContract):
    fame_to_datetime_conversion_triggered: bool = False

    def _configure_line_edit_for_unsigned_int(self, line_edit: QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegExp("\\d{1,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def _configure_line_edit_for_signed_int(self, line_edit: QLineEdit):
        line_edit.setText("0")
        regex_uint64 = QtCore.QRegExp("-?\\d{1,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))
        line_edit.textChanged.connect(self._update_ok_button_status)

    def _configure_line_edit_for_optional_signed_int(self, line_edit: QLineEdit):
        line_edit.setText("")
        line_edit.setPlaceholderText(self.tr("optional"))
        regex_uint64 = QtCore.QRegExp("-?\\d{0,20}")
        line_edit.setValidator(QtGui.QRegExpValidator(regex_uint64))

    def intersection(self, lst1, lst2):

        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    def format_list_item_sender(self, display_id, agent_type_name):
        return f"<li>Sender: agent <b>{display_id}</b> of type <b>{agent_type_name}</b></li> \n"

    def format_list_item_receiver(self, display_id, agent_type_name):
        return f"<li>Receiver: agent <b>{display_id}</b> of type <b>{agent_type_name}</b></li> \n"

    def __init__(
        self,
        sender: [],
        receiver: [],
        schema: models.Schema,
        parent=None,
    ):
        QDialog.__init__(self, parent)
        self._ui = Ui_DialogNewContract()
        self._ui.setupUi(self)
        self._sender: [AgentController] = sender
        self._receiver: [AgentController] = receiver

        self.setWindowTitle(self.tr("New contract"))
        sender_items = " ".join([self.format_list_item_sender(x.display_id, x.type_name) for x in self._sender])
        receiver_items = " ".join([self.format_list_item_receiver(x.display_id, x.type_name) for x in self._receiver])

        list_inner = sender_items + receiver_items

        self._ui.labelDescr.setText(
            self.tr(
                "<html><head/><body>"
                "<p>Create new contract between multiple Agents :</p>"
                f"<ul>{list_inner}"
                "</body></html>"
            )
        )

        # accept uint64 numbers as specified in protobuf schema
        self._configure_line_edit_for_unsigned_int(self._ui.lineDeliveryInterval)
        self._configure_line_edit_for_signed_int(self._ui.lineFirstDeliveryTime)
        self._configure_line_edit_for_optional_signed_int(self._ui.lineExpirationTime)

        # fill possible products to select based on the sender schema agent type
        sender_type_names = []
        receiver_type_names = []

        if len(self._sender) > 1 and len(self._receiver) != len(self._sender):
            QtWidgets.QMessageBox.warning(
                self,
                self.tr("Validation failure"),
                self.tr("The selected agents are not corresponding a one to many or  one to one schema \n\n"),
            )

            self.close()

            return

        for item in self._sender:
            sender_type = schema.agent_type_from_name(item.type_name)

            for product in sender_type.products:
                if sender_type_names.__contains__(product):
                    continue
                sender_type_names.append(product)

        for item in self._receiver:
            recv_type = schema.agent_type_from_name(item.type_name)

            for product in recv_type.products:
                if receiver_type_names.__contains__(product):
                    continue
                receiver_type_names.append(product)

        final_type_names = self.intersection(receiver_type_names, sender_type_names)

        self._ui.comboBoxProduct.addItems(final_type_names)

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(self._update_ok_button_status)
        self._update_ok_button_status()

        self._ui.lineFirstDeliveryNonFameTime.setCalendarPopup(True)
        self._ui.lineFirstDeliveryNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineFirstDeliveryNonFameTime.dateTimeChanged.connect(self._update_fame_times)
        self._ui.lineExpirationTimeNonFameTime.setCalendarPopup(True)
        self._ui.lineExpirationTimeNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineExpirationTimeNonFameTime.dateTimeChanged.connect(self._update_fame_times)

        self._ui.lineFirstDeliveryTime.textChanged.connect(self._update_fame_time_text_areas)
        self._ui.lineExpirationTime.textChanged.connect(self._update_fame_time_text_areas)

        # accept uint64 numbers as specified in protobuf schema
        self._configure_line_edit_for_unsigned_int(self._ui.lineDeliveryInterval)
        self._configure_line_edit_for_signed_int(self._ui.lineFirstDeliveryTime)
        self._configure_line_edit_for_optional_signed_int(self._ui.lineExpirationTime)

        # fill possible products to select based on the sender schema agent type

        # force the user to select a product except if only one is available
        if self._ui.comboBoxProduct.count() != 1:
            self._ui.comboBoxProduct.setCurrentIndex(-1)

        self._ui.comboBoxProduct.currentIndexChanged.connect(self._update_ok_button_status)
        self._update_ok_button_status()

        self._ui.lineFirstDeliveryNonFameTime.setCalendarPopup(True)
        self._ui.lineFirstDeliveryNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineFirstDeliveryNonFameTime.dateTimeChanged.connect(self._update_fame_times)
        self._ui.lineExpirationTimeNonFameTime.setCalendarPopup(True)
        self._ui.lineExpirationTimeNonFameTime.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self._ui.lineExpirationTimeNonFameTime.dateTimeChanged.connect(self._update_fame_times)

        self._ui.lineFirstDeliveryTime.textChanged.connect(self._update_fame_time_text_areas)
        self._ui.lineExpirationTime.textChanged.connect(self._update_fame_time_text_areas)

    def make_new_contracts(self) -> List[models.Contract]:

        expiration_time_str = self._ui.lineExpirationTime.text()
        expiration_time = int(expiration_time_str) if expiration_time_str else None

        if len(self._sender) == 1 and len(self._receiver) > 1:
            # One to many Contract Relationship
            sender = self._sender[0]

            return [
                models.Contract(
                    sender.id,
                    recv.id,
                    self._ui.comboBoxProduct.currentText(),
                    int(self._ui.lineDeliveryInterval.text()),
                    int(self._ui.lineFirstDeliveryTime.text()),
                    expiration_time,
                )
                for recv in self._receiver
            ]

        if len(self._sender) == len(self._receiver):
            # One to One Contract Relationship

            return [
                models.Contract(
                    sndr.id,
                    rec.id,
                    self._ui.comboBoxProduct.currentText(),
                    int(self._ui.lineDeliveryInterval.text()),
                    int(self._ui.lineFirstDeliveryTime.text()),
                    expiration_time,
                )
                for rec, sndr in zip(self._receiver, self._sender)
            ]
        # Not valid

        QtWidgets.QMessageBox.warning(
            self,
            self.tr("Validation failure"),
            self.tr("The selected agents are not corresponding a one to many or a one to one schema \n\n"),
        )

        return None
