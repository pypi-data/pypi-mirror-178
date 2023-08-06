import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Window 2.2
import QtGraphicalEffects 1.12
import QtQuick.Dialogs 1.0

import "qrc:/resources/js/desktop/popups.js" as Popups


FileDialog {
    id: fileDialog
    title: tr.select_image
    folder: shortcuts.home
    nameFilters: [ "Images (*.jpg *.jpeg *.png)" ]

    property var target: null
    property var isRounded: true

    onAccepted: {
        Popups.image_popup(target, imageFileDialog.fileUrl, isRounded)
        target = null
        imageFileDialog.close()
    }

    onRejected: {
        target = null
        imageFileDialog.close()
    }
}