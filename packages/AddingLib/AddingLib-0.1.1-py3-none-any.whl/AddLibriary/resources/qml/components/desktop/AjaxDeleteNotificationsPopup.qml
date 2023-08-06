import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.Dialog {
    id: popup

    property var callback: null
    property var confirmText: ""

    width: 320

    title: tr.information
    text: confirmText
    firstButtonCallback: callback
    firstButtonText: tr.ok
    secondButtonText: tr.cancel
}
