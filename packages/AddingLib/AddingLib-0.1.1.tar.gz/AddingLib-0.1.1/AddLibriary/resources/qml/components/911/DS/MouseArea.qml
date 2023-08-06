import QtQuick 2.12
import QtQuick.Controls 2.13


// Custom mouse area with pointing hand cursor and hover enabled
MouseArea {
    anchors.fill: parent
    hoverEnabled: true
    cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
}
