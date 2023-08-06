import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


// Input area for multiline text
Item {
    id: inputField

//  Title that places above the area
    property alias title: titleItem.text
//  Text in the area
    property alias value: valueItem.text
//  Title that places below the area
    property alias info: infoItem.text
//  If input is enabled
    property alias enabled: valueItem.enabled
//  Width of the area
    property alias areaWidth: valueItem.width
//  Height of the area
    property alias areaHeight: valueItem.height
//  Error that is shown when length rules are violated
    property string lengthError: ""
//  The most important error that should be set at runtime. (Preferably on the server response with error)
//  It will disappear when field loses focus
    property string forcedError: ""
//  Minimum length. If the text length is less than this value, it will cause length error
    property var minimumLength: 0
//  Maximum length of the value
    property var maximumLength: Number.MAX_NUMBER
//  If value is required. If true, then title will get additional sign `*`
    property bool required: false
//  If value has got changes and it makes sense to save it
    property bool readyToSave: value.trim() != valueItem.initValue

//  method to check if the value is valid
    function checkValid() {
        forcedError = ""
        if (!value.trim()) errorItem.text = required ? tr.field_cant_be_empty : ""
        else if (value.length < minimumLength) errorItem.text = lengthError
        else errorItem.text = ""
        return !errorItem.text
    }

//  Value editing has been finished
    signal editFinished
//  Focus of the area has been changed
    signal activeFocusChanged

    width: parent.width
    height: column.height

    Column {
        id: column

        width: parent.width
        height: titleItem.height + infoItem.height + areaWrapper.height

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
            id: areaWrapper

            width: parent.width
            height: valueItem.height + 4 + errorItem.height

            TextArea {
                id: valueItem

                property var initValue

                Component.onCompleted: initValue = text

                width: inputField.fieldWidth
                height: contentHeight + 2 * topPadding > implicitHeight ? contentHeight + 2 * topPadding : implicitHeight

                implicitHeight: 2 * topPadding + 38
                color: ui.colors.base
                wrapMode: TextEdit.Wrap
                font.pixelSize: 16
                font.family: roboto.name
                opacity: enabled ? 1 : 0.3
                selectByMouse: true
                selectionColor: ui.colors.interactive
                verticalAlignment: TextEdit.AlignTop
                topPadding: 12
                rightPadding: 8

                cursorDelegate: DS.Cursor {}

                background: Rectangle {
                    implicitWidth: 400
                    implicitHeight: 40
                    color: ui.backgrounds.highest
                    border.color: !errorItem.text ? ui.colors.interactive : ui.colors.attention
                    border.width: parent.activeFocus || !!errorItem.text ? 1 : 0
                    radius: 8
                }

                onEditingFinished: editFinished()
                onTextChanged: if (length > maximumLength) remove(maximumLength, length);
                onActiveFocusChanged: {
                    inputField.activeFocusChanged()
                    if (!valueItem.activeFocus) checkValid()
                }
            }

            DS.Text {
                id: errorItem

                width: valueItem.width
                height: visible ? contentHeight : 0

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

            height: text ? contentHeight : 0

            size: 14
            line: 20
            color: ui.colors.nonessential
        }
    }
}
