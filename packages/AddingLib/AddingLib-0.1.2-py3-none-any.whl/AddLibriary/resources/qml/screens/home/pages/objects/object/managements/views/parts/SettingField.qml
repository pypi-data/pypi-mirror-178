import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12
import "qrc:/resources/qml/components/desktop/" as Custom

Item {
    id: settingField

    width: parent.width
    // need height: 40
    height: {
        if (propName.contentHeight > propValue.contentHeight) {
            return propName.contentHeight + 23
        } else {
            return propValue.contentHeight + 23
        }
    }

    property bool hasRightIcon: false
    property bool bad: false
    property string sourceIcon: ""
    property string propertyName: ""
    property string propertyValue: ""
    property var upIconColor: bad ? ui.colors.attention : ui.colors.nonessential
    property var sourceIconGrayOpacity: 1.0
    property var halfWidth: width / 2 - 40

    property bool copyable: false
    function copy() {
        util.set_clipboard_text(propertyValue)
    }

    property alias propName: propName
    property alias propValue: propValue

    Custom.AjaxIcon {
        id: icon

        width: 24
        height: 24

        iconSource: sourceIcon
        iconColor: upIconColor

        opacity: sourceIconGrayOpacity

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 10
        }
    }

    Text {
        id: propName

        width: propValueAlt.contentWidth < settingField.halfWidth ? settingField.halfWidth * 2 - propValue.contentWidth - 1 : settingField.halfWidth - 1

        text: propertyName
        elide: Text.ElideRight
        wrapMode: Text.WordWrap

        color: bad ? ui.colors.attention : ui.colors.contrast
        font.pixelSize: 14
        font.family: roboto.name
        opacity: 0.8

        anchors {
            verticalCenter: parent.verticalCenter
            left: icon.right
            leftMargin: 12
        }
    }

    Text {
        id: propValue

        width: propValueAlt.contentWidth < settingField.halfWidth * 2 - propName.contentWidth ? propValueAlt.contentWidth + 1 : settingField.halfWidth * 2 - propName.contentWidth + 1

        text: propertyValue
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignRight

        color: bad ? ui.colors.attention : ui.colors.contrast
        font.pixelSize: 14
        font.family: roboto.name

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: hasRightIcon ? 40 : 10
        }
    }

    Text {
        id: propValueAlt
        text: propertyValue
        visible: false

        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignRight

        color: ui.colors.light1
        font.pixelSize: 14
        font.family: roboto.name

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 10
        }
    }
    MouseArea {
        id: copyArea

        visible: copyable
        anchors.fill: propValue
        hoverEnabled: true
        onEntered: propValue.color = ui.colors.green1
        onExited: propValue.color = ui.colors.contrast
        ToolTip {
            id: tooltip
            parent: parent

            contentItem: Text {
                text: tr.copied
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.light1
            }

            background: Rectangle {
                color: "#242424"
                radius: 4
                border {
                    width: 1
                    color: ui.colors.green1
                }
            }
        }
        onClicked: {
            copy()
            tooltip.show("", 500)
        }
    }
}
