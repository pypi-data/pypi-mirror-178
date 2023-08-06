import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "updatePopup"
    width: 440
    height: columnLayout.height
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    property var update_data: {"changelog": ["1", "2", "3"], "version": "0.666"}

    anchors.centerIn: parent

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        id: rect
        anchors.fill: parent
        border.width: 1
        color: ui.colors.dark3
        radius: 8

        Column {
            id: columnLayout

            Item {
                width: rect.width
                height: 48
            }

            Item {
                width: rect.width
                height: 64

                Image {
                    sourceSize.width: 67
                    sourceSize.height: 28
                    width: 67
                    height: 28
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/logo-pants-white.svg"
                }
            }

            Item {
                width: rect.width
                height: 32

                Custom.FontText {
                    text: popup.update_data.version
                    color: ui.colors.light1
                    anchors.centerIn: parent
                    font.pixelSize: 16
                }
            }

            Item {
                width: rect.width
                height: bodyItem.contentHeight + 24

                Custom.FontText {
                    id: bodyItem
                    width: parent.width - 32
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                    text: tr.new_version_downloaded_911
                    color: ui.colors.light1
                    anchors.centerIn: parent
                    font.pixelSize: 16
                }
            }

            Item {
                width: rect.width
                height: 32
            }

            Item {
                width: rect.width
                height: listView.height

                ListView {
                    id: listView
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: rect.width - 64
                    height: {
                        if (contentHeight < 256) return contentHeight
                        return 256
                    }

                    model: {
                        return popup.update_data.changelog
                    }
                    clip: true
                    spacing: 1

                    delegate: Item {
                        width: listView.width
                        height: (textItem.contentHeight > 40) ? textItem.contentHeight + 16 : 40

                        RowLayout {
                            anchors.fill: parent
                            Item {
                                Layout.preferredWidth: 24
                                Layout.preferredHeight: 40
                                Image {
                                    sourceSize.width: 24
                                    sourceSize.height: 24
                                    width: 24
                                    height: 24
                                    source: "qrc:/resources/images/icons/a-success-badge.svg"
                                    anchors.centerIn: parent
                                }
                            }

                            Item {
                                Layout.preferredWidth: 8
                            }

                            Item {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Custom.FontText {
                                    id: textItem
                                    width: parent.width - 10
                                    height: contentHeight
                                    text: listView.model[index]
                                    color: ui.colors.light1
                                    verticalAlignment: Text.AlignVCenter
                                    wrapMode: Text.WordWrap
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                            }
                        }
                    }
                }
            }

            Item {
                width: rect.width
                height: 32
            }

            Item {
                width: rect.width
                height: 1

                Rectangle {
                    width: parent.width - 32
                    height: 1
                    anchors.horizontalCenter: parent.horizontalCenter
                    color: ui.colors.dark1
                }
            }

            Item {
                width: rect.width
                height: 80

                Item {
                    width: parent.width - 32
                    height: parent.height - 32
                    anchors.centerIn: parent
                    RowLayout {
                        anchors.fill: parent

                        Item {
                            Layout.preferredWidth: 8
                        }

                        Custom.Button {
                            color: ui.colors.white
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            transparent: true
                            text: tr.remind_me_later

                            onClicked: {
                                updater.remind_later()
                                popup.close()
                            }
                        }

                        Item {
                            Layout.preferredWidth: 8
                        }

                        Custom.Button {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            transparent: true
                            text: tr.restart_app_now

                            onClicked: {
                                updater.install()
                            }
                        }

                        Item {
                            Layout.preferredWidth: 8
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: updater

        onInstallationStarted: {
            popup.close()
        }
    }
}