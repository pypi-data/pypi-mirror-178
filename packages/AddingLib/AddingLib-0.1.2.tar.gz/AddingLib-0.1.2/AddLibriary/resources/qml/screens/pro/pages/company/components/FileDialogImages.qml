import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.0

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


FileDialog {
    id: fileDialog

    folder: shortcuts.home
    title: tr.a911_choose_photo
    nameFilters: ["Image files (*.jpg *.png *.jpeg *.JPG *.PNG *.JPEG)"]

    onAccepted: {
        fileDialog.close()
    }

    onRejected: {
        fileDialog.close()
    }
}
