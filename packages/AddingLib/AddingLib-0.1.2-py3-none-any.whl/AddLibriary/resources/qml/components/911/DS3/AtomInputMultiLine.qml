import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


TextArea {
    id: textArea

//  Title that places above the field
    property alias label: labelItem.text
//  Whether the value from the field is required
    property bool required: false
//  If spinner id visible
    property bool hasSpinner: false
//  When need to use label item
    property alias labelItem: labelItem
//  Maximum length
    property int maximumLength

    width: 300
    height: contentHeight + labelItem.height

    onTextChanged: {
        if (!!maximumLength && text.length > maximumLength) {
            text = text.slice(0, maximumLength)
        }
    }

    color: enabled ? ui.ds3.figure.base : ui.ds3.figure.disabled
    placeholderTextColor: ui.ds3.figure.disabled
    font.pixelSize: 16
    font.family: roboto.name
    bottomPadding: 0
    topPadding: 0
    leftPadding: 0
    rightPadding: 0
    selectByMouse: true
    selectionColor: ui.ds3.figure.interactive
    verticalAlignment: labelItem.visible ? TextInput.AlignBottom : TextInput.AlignVCenter
    cursorDelegate: DS3.Cursor {}
    background: Item {}
    wrapMode: TextEdit.Wrap

    DS3.Text {
        id: labelItem

        width: parent.width
        height: visible ? contentHeight : 0

        anchors.top: parent.top

        visible: !!text
        style: ui.ds3.text.body.MRegular
        color: ui.ds3.figure.secondary
    }

    DS3.Spinner {
        size: DS3.Spinner.ImageSize.S

        anchors {
            right: textArea.right
            bottom: background.bottom
            rightMargin: 4
            bottomMargin: 4
        }

        visible: hasSpinner
    }
}
