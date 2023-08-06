import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// version: Athena 4.6
DS3.InputSingleLine {
    id: inputSingleLine

//  The code picker element
    property alias codePicker: codePicker
//  The phone number
    readonly property var phoneNumber: codePicker.codeText + atomInput.text

    height: inputsColumn.height +
        atomTitle.height +
        (!!errorText ? 8 + inputPhoneNumberCommentError.height : 0) +
        28

    showCommentError: false
    color: !atomInput.activeFocus && !codePicker.activeFocus || atomInput.readOnly ? ui.ds3.bg.highest : ui.ds3.bg.high

    inputsColumn {
        anchors {
            left: codePicker.right
            leftMargin: 4
            top: atomTitle.bottom
        }
    }

    atomInput {
        required: true
        labelItem.style: ui.ds3.text.body.LRegular

        validator: RegExpValidator { regExp: ui.regexes.phoneNoCode }
    }

    DS3.AtomTitle {
        id: atomTitle

        height: 20

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 16
        }

        title: tr.phone
        isPrimary: false
    }

    DS3.MasterCodePicker {
        id: codePicker

        sheetActionWidth: parent.width

        anchors {
            top: atomTitle.bottom
            topMargin: 9
            left: parent.left
            leftMargin: 16
        }

        popup {
            y: codePicker.height + 24 + ( inputPhoneNumberCommentError.visible ? 8 + inputPhoneNumberCommentError.height : 0 )
            x: -16
        }
    }

    Rectangle {
        id: underLine

        height: 1

        anchors {
            top: codePicker.bottom
            topMargin: 6
            right: codePicker.right
            left: codePicker.left
        }

        color: {
            if (!isValid) return ui.ds3.figure.attention
            return (enabled && !atomInput.activeFocus || atomInput.readOnly) ?
                ui.ds3.figure.disabled :
                ui.ds3.figure.secondary
        }
        opacity: enabled ? 1 : 0.3
    }

    DS3.Text {
        id: inputPhoneNumberCommentError

        anchors {
            top: underLine.bottom
            topMargin: 4
            left: inputSingleLine.left
            leftMargin: 16
            right: inputSingleLine.right
            rightMargin: 16
        }

        visible: !!errorText
        color: ui.ds3.figure.attention
        style: ui.ds3.text.body.SRegular
        text: errorText
        opacity: enabled ? 1 : 0.3
    }
}