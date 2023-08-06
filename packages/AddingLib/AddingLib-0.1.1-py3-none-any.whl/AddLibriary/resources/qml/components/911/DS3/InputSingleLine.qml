import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Main input
    property alias atomInput: atomInput
//  If you want to change right icon
    property alias rightIcon: rightIcon
//  If bad input
    readonly property bool isValid: !commentError.text
//  Validator error
    property var validatorError: ""
//  Length error
    property var lengthError: ""
//  Regex to validate the content on focus lost. Do not use with `atomInput.validator` property
    property var regex
//  Apply field validation ONLY when field has not active focus
    property bool hasValidationOnFocusLost: false
//  In case where data can only be entered through an external tool
    property bool allowClickIconWhenReadOnly: false
//  Comment error element
    property alias errorText: commentError.text
//  Column element for assigning new borders
    property alias inputsColumn: column
//  A bool value to determine if the commentError is shown
    property bool showCommentError: true

    function checkValid() {
        if (!!regex) atomInput.validator.regExp = regex
        if (!atomInput.text.trim() && atomInput.required) {
            commentError.text = tr.field_cant_be_empty
        } else if (!atomInput.acceptableInput) {
            commentError.text = validatorError.length ? validatorError : tr.incorrect_value
        } else if (atomInput.text.length > atomInput.maximumLength) {
            commentError.text = lengthError ? lengthError : tr.incorrect_value
        } else {
            commentError.text = ""
        }
        if (hasValidationOnFocusLost) atomInput.validator.regExp = /.*/
        return isValid
    }

    signal rightIconClicked

    Component.onCompleted: atomInput.text = atomInput.text // to cancel property binding

    onRegexChanged: atomInput.validator.regExp = regex

    width: parent.width
    height: column.height + 16

    color: !atomInput.activeFocus || atomInput.readOnly ? ui.ds3.bg.highest : ui.ds3.bg.high

    Column {
        id: column

        width: parent.width

        spacing: 4
        opacity: enabled ? 1 : 0.3

        anchors {
            top: parent.top
            topMargin: 8
            left: parent.left
            right: rightIconWrapper.visible ? rightIconWrapper.left : parent.right
            leftMargin: 16
            rightMargin: rightIconWrapper.visible ? 0 : 16
        }

        DS3.AtomInput {
            id: atomInput

            width: parent.width

            required: true
            rightPadding: 2 // to compensate for the cursor
            color: ui.ds3.figure.base
            validator: RegExpValidator {
                regExp: regex ? regex : /.*/
            }

            onTextEdited: commentError.text = ""
            onActiveFocusChanged:
            {
                if (hasValidationOnFocusLost && regex) validator.regExp = activeFocus ? /.*/ : regex
                if (!activeFocus) {
                    checkValid()
                    ensureVisible(0)
                }
            }

            Keys.onPressed: {
                if (event.key == Qt.Key_Up) {
                    atomInput.cursorPosition = 0
                    event.accepted = true
                } else if (event.key == Qt.Key_Down) {
                    atomInput.cursorPosition = atomInput.text.length
                    event.accepted = true
                }
            }
        }

        Rectangle {
            id: underLine

            height: 1

            anchors {
                right: atomInput.right
                left: atomInput.left
            }

            color: {
                if (isValid) {
                    if (enabled && !atomInput.activeFocus || atomInput.readOnly) return ui.ds3.figure.disabled
                    return ui.ds3.figure.secondary
                }
                return ui.ds3.figure.attention
            }
        }

        DS3.Text {
            id: commentError

            anchors {
                left: atomInput.left
                right: atomInput.right
            }

            visible: !!text && showCommentError
            color: ui.ds3.figure.attention
            style: ui.ds3.text.body.SRegular
        }
    }

    DS3.MouseArea {
        id: rightIconWrapper

        width: 56
        height: parent.height

        anchors {
            right: parent.right
            bottom: parent.bottom
            top: parent.top
            fill: undefined
        }

        visible: !!rightIcon.source.toString() && rightIcon.visible && (!atomInput.readOnly || allowClickIconWhenReadOnly)

        onClicked: rightIconClicked()
    }

    DS3.Icon {
        id: rightIcon

        anchors.centerIn: rightIconWrapper

        opacity: enabled ? 1 : 0.3
        color: ui.ds3.figure.interactive
    }
}
