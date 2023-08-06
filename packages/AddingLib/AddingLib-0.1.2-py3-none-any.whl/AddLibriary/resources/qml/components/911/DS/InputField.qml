import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


Item {
    id: inputField

//  Title that places above the field
    property alias title: titleItem.text
//  Text in the field
    property alias value: valueItem.text
//  Title that places below the field
    property alias info: infoItem.text
//  Placeholder text
    property alias placeholder: valueItem.placeholderText
//  If input is enabled
    property alias enabled: valueItem.enabled
//  Validator of the value. If it is set, then `regex` property will not make a sense
    property alias validator: valueItem.validator
//  If value is acceptable
    property alias acceptableInput: valueItem.acceptableInput
//  Maximum length of the value
    property alias maximumLength: valueItem.maximumLength
//  Minimum length. If the text length is less than this value, it will cause length error
    property var minimumLength: 0
//  Width of the field
    property var fieldWidth: 400
//  Error that is shown when length rules are violated
    property string lengthError: ""
//  Regex to validate the content on focus lost. Do not use with `validator` property
    property var regex
//  Error that is shown when validator rules are violated
    property string validatorError: ""
//  If value is required. If true, then title will get additional sign `*`
    property bool required: false
//  Condition of the plus button visibility
    property bool hasPlusButton: false
//  Condition of the minus button visibility
    property bool hasMinusButton: false
//  If value has got changes and it makes sense to save it
    property bool readyToSave: value.trim() != valueItem.initValue
//  If value need confirmation. If true, then there will be confirmation text button on the right of the field
    property bool confirmation
//  If true, then only one item of the following can be visible: errorItem, infoItem. The last has highest priority
    property bool isJointBottomText
//  The most important error that should be set at runtime. (Preferably on the server response with error)
//  It will disappear when field loses focus
    property string forcedError: ""
//  The value item
    readonly property alias valueItem: valueItem
//  Contains true if there are no errors and value is valid
    readonly property bool valid: !errorItem.text
//  Contains true when the field has active focus
    readonly property bool hasFocus: valueItem.activeFocus

//  Method to set focus on the field
    function forceActiveFocus() {
        valueItem.forceActiveFocus()
    }

//  method to check if the value is valid
    function checkValid() {
        forcedError = ""
        if (!value.trim()) errorItem.text = required ? tr.field_cant_be_empty : ""
        else if (!acceptableInput) errorItem.text = validatorError
        else if (value.length < minimumLength) errorItem.text = lengthError
        else errorItem.text = ""
        return !errorItem.text
    }

//  Value has been edited
    signal edited
//  Text selection has been changed
    signal selected
//  Confirmation signal. Makes sense when confirmation is true
    signal confirm
//  Plus button click
    signal plusClicked
//  Minus button click
    signal minusClicked
//  Value editing has been finished
    signal editFinished

    onForcedErrorChanged: errorItem.text = forcedError

    width: parent.width
    height: column.height

    Column {
        id: column

        width: parent.width

        spacing: 8

        DS.Text {
            id: titleItem

            height: text ? contentHeight : 0

            size: 14
            line: 20
            color: ui.colors.secondary

            Component.onCompleted: {
                if (required && !!text) text += ui.required
            }
        }

        Item {
            width: parent.width
            height: valueItem.height + errorItem.height

            TextField {
                id: valueItem

                property var initValue

                Component.onCompleted: initValue = text

                width: Math.min(inputField.fieldWidth, inputField.width)
                height: background.height

                rightPadding: hasMinusButton ? 40 : 8
                color: ui.colors.base
                placeholderTextColor: ui.colors.disabled
                font.pixelSize: 16
                font.family: roboto.name
                opacity: enabled ? 1 : 0.3
                selectByMouse: true
                selectionColor: ui.colors.interactive
                validator: RegExpValidator {
                    id: regexValidator

                    regExp: /.*/
                }

                cursorDelegate: DS.Cursor {}

                background: Rectangle {
                    implicitWidth: 400
                    implicitHeight: 40
                    color: ui.backgrounds.highest
                    border.color: !errorItem.text ? ui.colors.interactive : ui.colors.attention
                    border.width: parent.activeFocus || !!errorItem.text ? 1 : 0
                    radius: 8
                }

                DS.ButtonRound {
                    anchors {
                        right: valueItem.right
                        rightMargin: 9
                        verticalCenter: valueItem.verticalCenter
                    }

                    style: ui.controls.minus
                    visible: hasMinusButton

                    onClicked: minusClicked()
                }

                DS.ButtonRound {
                    id: plusButton

                    anchors {
                        right: valueItem.right
                        rightMargin: -32
                        verticalCenter: valueItem.verticalCenter
                    }

                    style: ui.controls.plus
                    visible: hasPlusButton && valueItem.acceptableInput

                    onClicked: plusClicked()
                }

                DS.Text {
                    anchors {
                        verticalCenter: valueItem.verticalCenter
                        left: plusButton.visible ? plusButton.right : valueItem.right
                        leftMargin: 8
                    }

                    width: contentWidth
                    x: inputField.fieldWidth + 8
                    visible: confirmation
                    color: ui.colors.interactive
                    text: tr.confirm

                    DS.MouseArea {
                        onClicked: confirm()
                    }
                }

                Keys.onEscapePressed: parent.forceActiveFocus()
                Keys.onReturnPressed: nextItemInFocusChain().forceActiveFocus()

                onTextEdited: edited()
                onEditingFinished: editFinished()
                onActiveFocusChanged: {
                    if (regex) regexValidator.regExp = activeFocus ? /.*/ : regex
                    if (!valueItem.activeFocus) checkValid()
                }
                onSelectedTextChanged: selected()
            }

            DS.Text {
                id: errorItem

                width: valueItem.width
                height: visible ? contentHeight + 4 : 0

                anchors {
                    top: valueItem.bottom
                    topMargin: 4
                }

                visible: !!text
                size: 14
                line: 20
                color: ui.colors.attention
            }
        }

        DS.Text {
            id: infoItem

            width: parent.width
            height: text ? contentHeight : 0

            size: 14
            line: 20
            color: ui.colors.nonessential
            visible: isJointBottomText ? !errorItem.visible : true
        }
    }
}
