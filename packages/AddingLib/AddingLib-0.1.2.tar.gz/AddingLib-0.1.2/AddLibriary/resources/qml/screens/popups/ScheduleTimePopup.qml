import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "scheduleTimePopup"
    width: parent.width
    height: parent.height
    closePolicy: Popup.CloseOnPressOutside

    onParentChanged: {
        if (parent) {
            popup.width = parent.width
            popup.height = parent.height
        }
    }

    focus: true
    modal: false

    property var updateBody: null

    anchors.centerIn: null

    x: 0
    y: 0

    onOpened: {
        timeField.control.forceActiveFocus(true)
    }

    onAboutToHide: {
        if (!popup.parent) return
        popup.parent.bodyText.text = util.normalize_time(timeField.control.text)
        updateBody.updateModel()
    }

    background: Item {}

    contentItem: Item {
        anchors.fill: parent

        Custom.TextField {
            id: timeField
            width: parent.width
            height: parent.height
            placeHolderText: "00:00"
            control.leftPadding: 16
            control.text: popup.parent.bodyText.text
            background.radius: 10
            background.color: ui.colors.dark1
            background.height: height
            control.inputMask: "00:00"
            control.validator: RegExpValidator { regExp: /^((0[0-9 ]|1[0-9 ]|2[0-3 ]|  ):[0-5 ][0-9 ])|(24:[0-0 ][0-0 ])$/ }
            anchors {
                centerIn: parent
                verticalCenterOffset: 4
            }

            control.onTextChanged: {
                timeField.control.text = timeField.control.text
                popup.parent.bodyText.text = util.normalize_time(timeField.control.text)
            }
        }
    }
}
