import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    anchors.fill: parent
    color: ui.colors.dark3

    Connections {
        target: app.company_module

        onCompanyCreated: {
            companyLoader.setSource("qrc:/resources/qml/screens/pro/pages/company/Wait.qml")
        }
    }

    Rectangle {
        id: backPanel
        color: ui.colors.black
        width: 64
        height: parent.height
        anchors.left: parent.left

        Image {
            sourceSize.width: 24
            sourceSize.height: 24
            source: "qrc:/resources/images/icons/back-arrow.svg"
            anchors {
                top: parent.top
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        Custom.HandMouseArea {
            onClicked: {
                application.debug("pro -> company -> back to start company creation")
                companyLoader.setSource("qrc:/resources/qml/screens/pro/pages/company/Create.qml")
            }
        }
    }

    ScrollView {
        id: scrollView
        clip: true
        anchors {
            top: parent.top
            left: backPanel.right
            right: parent.right
            bottom: parent.bottom
        }

        ScrollBar.vertical.policy: {
            if (scrollView.contentHeight > scrollView.height) {
                return ScrollBar.AlwaysOn
            }
            return ScrollBar.AlwaysOff
        }

        PropertyAnimation {
            id: scrollBarAnim
            target: scrollView.ScrollBar.vertical
            to: 0
            duration: 400
            property: "position"
            property var action: null

            onFinished: {
                if (scrollBarAnim.action) {
                    scrollBarAnim.action()
                    scrollBarAnim.action = null
                }
            }
        }
        RowLayout {
            spacing: 0
            width: scrollView.width

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 76
            }

            ColumnLayout {
                id: columnLayout
                spacing: 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 1000

                Rectangle {
                    id: header
                    color: "transparent"
                    Layout.fillWidth: true
                    Layout.minimumHeight: 104
                    Layout.maximumHeight: 104

                    Custom.FontText {
                        text: tr.a911_create_company_application
                        width: parent.width
                        color: ui.colors.white
                        font.pixelSize: 32
                        opacity: 0.9
                        anchors.centerIn: parent
                    }
                }

                Rectangle {
                    id: body
                    color: ui.colors.green1
                    Layout.fillWidth: true
                    Layout.minimumHeight: companyInfo.height
                    Layout.maximumHeight: companyInfo.height

                    CompanyInfo {
                        id: companyInfo
                        width: parent.width
                        anchors.top: parent.top
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: 140
            }
        }
    }
}