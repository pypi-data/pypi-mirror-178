import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Default text
Text {
    id: textItem

//  Whether text elides or wraps
    property bool hasElide: false
//  Whether text is clickable
    property bool isClickable: false
//  Style of the text from the presets in ui.ds3.text...
    property var style: ui.ds3.text.body.MRegular
//  Text click callback
    property var action: () => {}

    height: contentHeight

    color: ui.ds3.figure.base
    font.letterSpacing: style.size / 10 - 1
    font.family: roboto.name
    font.pixelSize: style.size
    font.weight: style.weight
    font.capitalization: !!style.uppercase ? Font.AllUppercase : Font.MixedCase
    lineHeight: style.height
    lineHeightMode: Text.FixedHeight
    verticalAlignment: Text.AlignVCenter
    horizontalAlignment: Text.AlignLeft
    wrapMode: Text.Wrap
    elide: hasElide ? Text.ElideRight : Text.ElideNone

    onHoveredLinkChanged: {
        infoArea.visible = !!hoveredLink
    }

    onLinkActivated: if (!link.startsWith("#")) Qt.openUrlExternally(link)

    DS3.MouseArea {
        id: infoArea

        visible: false

        acceptedButtons: Qt.NoButton
    }

    DS3.MouseArea {
        id: clickableArea

        visible: isClickable

        onClicked: action()
    }
}