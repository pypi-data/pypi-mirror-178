import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: moreAboutDesktop

    width: parent.width
    height: moreAboutDesktopItem.height + 16 + 90

    property var blockWidth: width / 3 - 8

    Item {
        id: moreAboutDesktopItem

        width: parent.width
        height: moreAboutDesktopText.contentHeight

        Desktop.NormalText {
            id: moreAboutDesktopText

            text: tr.onboarding_pro_desktop_title
            size: 24
            bold: true
            elideMode: true
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent
        }
    }

    Rectangle {
        width: moreAboutDesktop.blockWidth
        height: 90

        color: ui.colors.dark1
        radius: 10

        anchors {
            left: parent.left
            bottom: parent.bottom
        }

        Desktop.NormalText {
            width: parent.width - 32
            text: tr.get_started
            size: 12
            color: ui.colors.middle1

            anchors {
                top: parent.top
                topMargin: 12
                left: parent.left
                leftMargin: 16
            }
        }

        Desktop.NormalText {
            width: parent.width - 32
            text: tr.onboarding_pro_desktop_get_started
            size: 16
            bold: true
            elideMode: true
            color: ui.colors.light3

            anchors {
                left: parent.left
                leftMargin: 16
                bottom: parent.bottom
                bottomMargin: 12
            }
        }

        Image {
            source: "qrc:/resources/images/pro/company/arrow.svg"
            sourceSize {
                width: 16
                height: 16
            }

            anchors {
                top: parent.top
                topMargin: 12
                right: parent.right
                rightMargin: 16
            }
        }

        Custom.HandMouseArea {
            onClicked: {
                var link = "https://support.ajax.systems/" + companyStack.linkLocale + "/manuals/pro-desktop/"
                Qt.openUrlExternally(link)
            }
        }
    }

    Rectangle {
        width: moreAboutDesktop.blockWidth
        height: 90

        color: ui.colors.dark1
        radius: 10

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        Desktop.NormalText {
            width: parent.width - 32
            text: tr.a911_monitoring
            size: 12
            color: ui.colors.middle1

            anchors {
                top: parent.top
                topMargin: 12
                left: parent.left
                leftMargin: 16
            }
        }

        Desktop.NormalText {
            width: parent.width - 32
            text: tr.onboarding_pro_desktop_add_hubs
            size: 16
            bold: true
            elideMode: true
            color: ui.colors.light3

            anchors {
                left: parent.left
                leftMargin: 16
                bottom: parent.bottom
                bottomMargin: 12
            }
        }

        Image {
            source: "qrc:/resources/images/pro/company/arrow.svg"
            sourceSize {
                width: 18
                height: 18
            }

            anchors {
                top: parent.top
                topMargin: 12
                right: parent.right
                rightMargin: 16
            }
        }

        Custom.HandMouseArea {
            onClicked: {
                var link = "https://support.ajax.systems/" + companyStack.linkLocale + "/manuals/pro-desktop/#block9-1"
                Qt.openUrlExternally(link)
            }
        }
    }

    Rectangle {
        width: moreAboutDesktop.blockWidth
        height: 90

        color: ui.colors.dark1
        radius: 10

        anchors {
            right: parent.right
            bottom: parent.bottom
        }

        Desktop.NormalText {
            width: parent.width - 32
            text: tr.a911_company
            size: 12
            color: ui.colors.middle1

            anchors {
                top: parent.top
                topMargin: 12
                left: parent.left
                leftMargin: 16
            }
        }

        Desktop.NormalText {
            width: parent.width - 32
            text: tr.onboarding_pro_desktop_add_employees
            size: 16
            bold: true
            elideMode: true
            color: ui.colors.light3

            anchors {
                left: parent.left
                leftMargin: 16
                bottom: parent.bottom
                bottomMargin: 12
            }
        }

        Image {
            source: "qrc:/resources/images/pro/company/arrow.svg"
            sourceSize {
                width: 16
                height: 16
            }

            anchors {
                top: parent.top
                topMargin: 12
                right: parent.right
                rightMargin: 16
            }
        }

        Custom.HandMouseArea {
            onClicked: {
                var link = "https://support.ajax.systems/" + companyStack.linkLocale + "/manuals/pro-desktop/#block10-1"
                Qt.openUrlExternally(link)
            }
        }
    }
}
