import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: atomTitle

//  Whether title or subtitle is primary. If true, the title is primary
    property bool isPrimary: true
//  Whether texts are bold
    property bool isBold: false
//  Upper text
    property alias title: titleItem.text
//  Color of the title text
    property alias titleColor: titleItem.color
//  Bottom text
    property alias subtitle: subtitleItem.text
//  Color of the subtitle text
    property alias subtitleColor: subtitleItem.color
//  Text of the badge
    property alias badge: badgeLabel.text
//  Color of the badge
    property alias badgeColor: badgeLabel.outlineColor
//  Whether need to change Text
    property alias subtitleItem: subtitleItem
//  Whether need to read
    property alias titleItem: titleItem
//  Elide long Title or Subtitle text
    property alias elide: titleItem.elide
//  Component small icon
    property alias subtitleIcon: subtitleIcon

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleTitleName: ""
    property var accessibleSubtitleName: ""
    /* ---------------------------------------------------- */

    implicitWidth: 100
    height: Math.max(30, textBlock.height)

    Column {
        id: textBlock

        width: parent.width

        anchors.verticalCenter: parent.verticalCenter

        Item {
            height: titleItem.visible ? titleItem.height : 0
            width: parent.width

            DS3.Text {
                id: titleItem

                width: parent.width

                style: ui.ds3.text.body[(isPrimary ? "L" : "M") + (isBold && (isPrimary || !isPrimary && !subtitle) ? "Bold" : "Regular")]
                visible: text.length
                color: enabled ? ui.ds3.figure[isPrimary ? "base" : "secondary"] : ui.ds3.figure.nonessential

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: atomTitle.accessibleTitleName
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ---------------------------------------------------- */
            }
        }

        Row {
            width: parent.width

            spacing: 4

            DS3.Icon {
                id: subtitleIcon

                anchors.verticalCenter: parent.verticalCenter

                visible: !!source
                source: ""
            }

            DS3.Text {
                id: subtitleItem

                width: textBlock.width - subtitleIcon.width

                anchors.verticalCenter: parent.verticalCenter

                visible: !!text

                style: ui.ds3.text.body[(isPrimary ? "M" : "L") + (!isPrimary && isBold ? "Bold" : "Regular")]
                color: ui.ds3.figure[isPrimary ? "secondary" : "base"]
                elide: titleItem.elide
                wrapMode: titleItem.wrapMode

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: atomTitle.accessibleSubtitleName
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ---------------------------------------------------- */
            }
        }

        DS3.Spacing {
            height: badgeLabel.visible ? 8 : 0
        }

        DS3.BadgeLabel {
            id: badgeLabel

            visible: !!badge
            isOutline: true
        }
    }
}
