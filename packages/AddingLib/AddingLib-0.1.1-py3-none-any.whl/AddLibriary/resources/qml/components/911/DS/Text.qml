import QtQuick 2.12


// Default text
Text {
    id: text

//  Weight of the text
    property var weight: Font.Normal
//  Size of the text in pixels
    property var size: 14
//  Line height of the text
    property var line: 20
//  Whether text elides or wraps
    property bool hasElide: false
//  Whether text is clickable. Set false to do not cover mousearea of the parent
    property bool action: true

    height: contentHeight

    color: ui.colors.base
    font.family: roboto.name
    font.pixelSize: size
    font.weight: weight
    lineHeight: line
    lineHeightMode: Text.FixedHeight
    verticalAlignment: Text.AlignVCenter
    horizontalAlignment: Text.AlignLeft
    wrapMode: Text.Wrap
    elide: hasElide ? Text.ElideRight : Text.ElideNone

    onHoveredLinkChanged: {
        if (hoveredLink) infoArea.cursorShape = Qt.PointingHandCursor
        else infoArea.cursorShape = Qt.ArrowCursor
    }

    MouseArea {
        id: infoArea

        anchors.fill: parent

        visible: action

        onClicked: if (parent.hoveredLink) Qt.openUrlExternally(parent.hoveredLink)
    }
}
