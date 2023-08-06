import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Text {
    id: normalText

    text: ""
    color: ui.colors.white

    property var size: 14
    property var bold: false
    property var elideMode: false

    wrapMode: Text.Wrap
    elide: normalText.elideMode ? Text.ElideRight : Text.ElideNone
    textFormat: Text.PlainText
    verticalAlignment: Text.AlignVCenter

    font {
        family: roboto.name
        bold: normalText.bold
        pixelSize: normalText.size
    }
}
