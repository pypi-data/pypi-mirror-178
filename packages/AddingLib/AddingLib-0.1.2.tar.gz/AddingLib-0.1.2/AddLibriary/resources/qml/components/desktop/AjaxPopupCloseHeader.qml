import QtQuick 2.7
import QtQuick.Controls 2.2

Item {
    id: closeItem

    width: parent.width
    height: Math.max(settingsLabel.height + 14, 48)
    anchors {
        top: parent.top
    }
    property string label: ""
    property alias icoClose: icoClose
    property alias icoCloseArea: mouseArea
    property int fontSize: 20
    property var textOpacity: 1.0

    /* -------------------------------------------- */
    /* desktop tests */
    property var accessibleIcoName: ""
    property var accessibleTextName: ""
    property var accessibleAreaName: ""
    /* -------------------------------------------- */

    Image {
        id: icoClose

        source: "qrc:/resources/images/desktop/icons/ic-close.svg"
        width: 16
        height: 16
        opacity: 0.9
        anchors {
            top: parent.top
            topMargin: 14
            right: parent.right
            rightMargin: 16
        }

        MouseArea {
            id: mouseArea

            anchors.fill: icoClose
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: popup.close()
            onEntered: icoClose.opacity = 1.0
            onExited: icoClose.opacity = 0.9

            /* -------------------------------------------- */
            /* desktop tests */
            Accessible.name: closeItem.accessibleIcoName
            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + icoClose.source + "</button>"
            Accessible.role: Accessible.Button
            Accessible.checkable: visible && enabled
            Accessible.onPressAction: {
                if (!Accessible.checkable) return
                mouseArea.clicked(true)
            }
            /* -------------------------------------------- */
        }
    }

    Text {
        id: settingsLabel

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            topMargin: 14
        }

        width: parent.width - 80
        height: contentHeight

        text: label
        color: ui.colors.light1
        font.family: roboto.name
        font.pixelSize: fontSize
        wrapMode: Text.Wrap
        opacity: closeItem.textOpacity
        elide: {
            if (lineCount > 2) return Text.ElideRight
            return Text.ElideNone
        }
        horizontalAlignment: Text.AlignHCenter

        /* ------------------------------------------------ */
        /* desktop tests */
        Accessible.name: closeItem.accessibleTextName
        Accessible.description: text
        Accessible.role: Accessible.Paragraph
        /* ------------------------------------------------ */
    }

    /* ---------------------------------------------------- */
    /* desktop tests */
    Accessible.name: closeItem.accessibleAreaName
    Accessible.description: "popup header instance (group)"
    Accessible.role: Accessible.Grouping
    /* ---------------------------------------------------- */
}
