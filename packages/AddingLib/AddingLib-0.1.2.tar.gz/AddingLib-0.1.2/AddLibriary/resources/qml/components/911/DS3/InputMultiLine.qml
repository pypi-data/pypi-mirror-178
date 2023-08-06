import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Main input
    property alias atomInputMultiline: atomInputMultiline
//  If bad input
    readonly property bool isValid: !commentError.text
//  Validator error
    property var validatorError: ""
//  Length error
    property var lengthError: ""
//  Regex to validate the content on focus lost. Do not use with `atomInput.validator` property
    property var regex
//  Is input acceptable
    property alias acceptableInput: inputValidator.acceptableInput

    function checkValid() {
        if (!!regex) inputValidator.validator.regExp = regex
        if (!atomInputMultiline.text.trim() && atomInputMultiline.required) {
            commentError.text = tr.field_cant_be_empty
        } else if (!acceptableInput) {
            commentError.text = validatorError.length ? validatorError : tr.incorrect_value
        } else {
            commentError.text = ""
        }
        return isValid
    }

    Component.onCompleted: atomInputMultiline.text = atomInputMultiline.text // to cancel property binding

    width: parent.width
    height: column.height + 16

    color: !atomInputMultiline.activeFocus || atomInputMultiline.readOnly ? ui.ds3.bg.highest : ui.ds3.bg.high

    Column {
        id: column

        anchors {
            top: parent.top
            topMargin: 8
            left: parent.left
            right: parent.right
        }

        opacity: enabled ? 1 : 0.3
        spacing: 4

        DS3.AtomInputMultiLine {
            id: atomInputMultiline

            anchors {
                left: parent.left
                right: parent.right
                leftMargin: 16
                rightMargin: 16
            }

            required: true
            color: ui.ds3.figure.base

            onTextChanged: {
                commentError.text = ""
                if (!!maximumLength && text.length > maximumLength) {
                    text = text.slice(0, maximumLength)
                }
            }

            onActiveFocusChanged: {
                if (regex) inputValidator.validator.regExp = activeFocus ? /.*/ : regex
                if (!activeFocus) checkValid()
            }
        }

        Rectangle {
            id: underLine

            height: 1

            anchors {
                right: atomInputMultiline.right
                left: atomInputMultiline.left
            }

            color: {
                if (!isValid) return ui.ds3.figure.attention
                return enabled && !atomInputMultiline.activeFocus && !atomInputMultiline.readOnly ?
                    ui.ds3.figure.disabled :
                    ui.ds3.figure.secondary
            }
        }

        DS3.Text {
            id: commentError

            width: parent.width
            height: visible ? contentHeight : 0

            anchors {
                left: atomInputMultiline.left
                right: atomInputMultiline.right
            }

            visible: !!text
            color: ui.ds3.figure.attention
            style: ui.ds3.text.body.SRegular
        }
    }

    TextField {
        id: inputValidator

        text: atomInputMultiline.text

        validator: RegExpValidator {
            regExp: /.*/
        }
        visible: false
    }
}
