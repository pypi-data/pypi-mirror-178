import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12
import "qrc:/resources/qml/components/desktop/" as Custom

Item {
    width: parent.width
    height: {
        if (propName.contentHeight > propValue.contentHeight) {
            return propName.contentHeight + 23
        } else {
            return propValue.contentHeight + 23
        }
    }

    property bool bad: false

    property string sourceIcon: ""

    property string sourceIconGray: ""
    property string sourceIconRed: ""
    property string propertyName: ""
    property string propertyIconGray: ""
    property string propertyIconRed: ""
    property var sourceIconGrayOpacity: 1.0
    property var isna: false

    Custom.AjaxIcon {
        id: iconNew

        width: 24
        height: 24

        iconSource: sourceIcon
        iconColor: bad ? ui.colors.attention : ui.colors.nonessential

        opacity: sourceIconGrayOpacity

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 10
        }
    }

    Image {
        id: icon
        source: bad ? sourceIconRed : sourceIconGray

        width: 24
        height: 24

        visible: !sourceIcon
        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 10
        }
    }

    Text {
        id: propName

        text: propertyName
        width: ((parent.width - 48) * 4) / 5

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

    Image {
        id: propImage
        source: bad ? propertyIconRed : propertyIconGray
        width: 18
        height: 18
        opacity: 0.9
        visible: !isna

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 10
        }
    }

    Text {
        id: propValue
        text: tr.na

        visible: isna

        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignRight

        color: bad ? ui.colors.attention : ui.colors.contrast
        font.pixelSize: 14
        font.family: roboto.name

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 10
        }
    }
}
