from .Functions import get_system_autostart_path, get_user_autostart_path
from PyQt6.QtWidgets import QWidget, QListWidgetItem
from .AddEditDialog import AddEditDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import desktop_entry_lib
from PyQt6 import uic
import os


class MainWindow(QWidget):
    def __init__(self, app_icon: QIcon):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "MainWindow.ui"), self)

        self._add_edit_dialog = AddEditDialog(self)
        self._app_icon = app_icon

        self.update_desktop_list()

        self.desktop_list.itemChanged.connect(self._item_changed)
        self.desktop_list.itemSelectionChanged.connect(self._update_buttons_enabled)
        self.add_button.clicked.connect(self._add_edit_dialog.open_add_dialog)
        self.edit_button.clicked.connect(lambda: self._add_edit_dialog.open_edit_dialog(self.desktop_list.currentItem().data(42)))

    def update_desktop_list(self) -> None:
        col = desktop_entry_lib.DesktopEntryCollection()

        for i in (get_system_autostart_path(), get_user_autostart_path()):
            if os.path.isdir(i):
                col.load_directory(i)

        self.desktop_list.clear()

        for i in col.desktop_entries.values():
            item = QListWidgetItem(i.Name.get_translated_text())

            if i.Hidden:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)

            if i.Icon is not None:
                icon = QIcon.fromTheme(i.Icon)
                if icon.isNull():
                    item.setIcon(self._app_icon)
                else:
                    item.setIcon(QIcon.fromTheme(i.Icon))
            else:
                item.setIcon(self._app_icon)

            item.setData(42, i)
            item.setToolTip(i.Comment.get_translated_text())

            self.desktop_list.addItem(item)

        self.desktop_list.sortItems()
        self._update_buttons_enabled()

    def _item_changed(self, item: QListWidgetItem):
        entry: desktop_entry_lib.DesktopEntry = item.data(42)
        entry.Hidden = item.checkState() == Qt.CheckState.Unchecked
        entry.write_file(os.path.join(get_user_autostart_path(), entry.desktop_id + ".desktop"))

    def _update_buttons_enabled(self):
        if self.desktop_list.currentRow() == -1:
            self.edit_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            return

        self.edit_button.setEnabled(True)

        entry: desktop_entry_lib.DesktopEntry = self.desktop_list.currentItem().data(42)
        self.remove_button.setEnabled(not os.path.exists(os.path.join(get_system_autostart_path(), entry.desktop_id + ".desktop")))

    def _remove_button_clicked(self):
        entry: desktop_entry_lib.DesktopEntry = self.desktop_list.currentItem().data(42)
        os.remove(entry.file_path)
        self._update_buttons_enabled()
