import QtQuick.Dialogs 1.3
import QtQuick 2.12

FileDialog {
    id: fileDialog
    title: tr.a911_choose_photo
    folder: shortcuts.home
    nameFilters: ["Image files (*.jpg *.png *.jpeg *.JPG *.PNG *.JPEG)"]
    onAccepted: {

        fileDialog.close()
    }
    onRejected: {
        fileDialog.close()
    }
}