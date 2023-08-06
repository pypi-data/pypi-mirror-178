import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Rectangle {
    anchors.fill: parent
    color: ui.colors.dark3

    Item {
        id: phoneItem
        width: parent.width - 64
        height: 80
        anchors {
            top: parent.top
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }
        Custom.TextFieldEdit{
            id: phoneField
            distance: 20
            width: 192

            valueText.control.font.pixelSize: 16
            valueText.control.color: ui.colors.light3
            valueText.control.maximumLength: 30
            valueText.control.validator: RegExpValidator { regExp: /(\+|[0-9])?[0-9]+/ }
            key: tr.phone
            value: appUser.data.user_info.phone
            anchors {
                bottom: parent.bottom
            }
        }
        Custom.ComboBox {
            id: languageCombo
            width: 167
            model: ["Suomi", "Some text 2", "Some text 3"]

            copyVisible: false
            defaultText: "defaultText"
            backgroundRectangle.color: ui.colors.dark1
            anchors {
                left: phoneField.right
                leftMargin: 16
                bottomMargin: 8
                bottom: phoneField.bottom
            }
        }
    }
    Rectangle {
        id: delimiter
        width: parent.width - 32
        height: 1
        color: ui.colors.dark1
        anchors {
            top: parent.top
            topMargin: 109
            right: parent.right
        }
    }
    Item {
        id: emailItem
        width: parent.width - 64
        height: 80
        anchors {
            top: delimiter.bottom
            topMargin: 8
            horizontalCenter: parent.horizontalCenter
        }
        Custom.TextFieldEdit{
            id: emailField
            distance: 20
            width: parent.width
            valueText.control.font.pixelSize: 16
            valueText.control.color: ui.colors.light3
            valueText.control.maximumLength: 100
            key: tr.email
            value: appUser.data.user_info.email
        }
    }

    Rectangle {
        width: parent.width - 32
        height: 1
        color: ui.colors.dark1
        anchors {
            bottom: parent.bottom
            bottomMargin: 88
            right: parent.right
        }
    }

    Custom.Button {
        id: btnSaveChanges
        width: 376
        height: 40
        backgroundItem.border.color: btnSaveChanges.transparent ? "transparent" : ui.colors.green1
        transparent: !(phoneField.valueText.control.text && emailField.valueText.control.text)

        color: !btnSaveChanges.transparent ? ui.colors.green1 : "white"
        text: tr.a911_save_changes
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            bottomMargin: 16
        }
    }
}