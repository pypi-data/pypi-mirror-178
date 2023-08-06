import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.3


Item {
    id: playerPanel

    FontLoader { id: roboto; source: "qrc:/resources/fonts/Roboto-Regular.ttf" }

    property var streamData: null
    property var snapshotPath: ""

    property var channelsData: null
    property var currentChannel: null

    Rectangle {
        anchors.fill: parent
        color: "#1d1d1d"
    }

    Rectangle {
        anchors.fill: parent
        color: "#373737"
        radius: 16

        Text {
            id: camType
            color: "#fdfdfd"
            opacity: 0.65
            font.family: "Open Sans"
            font.letterSpacing: 1
            font.pixelSize: 14
            wrapMode: Text.WordWrap
            anchors {
                left: parent.left
                leftMargin: 30
                top: parent.top
                topMargin: {
                    if (channelsData && channelsData != [] && scrollBar.policy == ScrollBar.AlwaysOn) return 4
                    if (channelsData && channelsData != [] && scrollBar.policy == ScrollBar.AlwaysOff) return 6
                    return 14
                }
            }

            text: {
                if (!streamData) return ""
                if (streamData.camera.type == "NO_SERVICE_TYPE_INFO") return ""

                if (streamData.camera.type == "RTSP_STREAM") return "RTSP Camera"
                if (streamData.camera.type == "XMEYE") return "XMeye"
                if (streamData.camera.type == "HIKVISION") return "Hikvision"
                if (streamData.camera.type == "DAHUA") return "Dahua"
                if (streamData.camera.type == "SAFIRE") return "Safire"
                if (streamData.camera.type == "UNIVIEW") return "Uniview"
                if (streamData.camera.type == "IVIDEON") return "iVideon"

                return ""
            }
        }

        Text {
            id: camInfo
            width: control.x - camInfo.x - 20
            color: "#fdfdfd"
            opacity: 0.9
            font.family: "Open Sans"
            font.letterSpacing: 1
            font.pixelSize: 16
            font.bold: true
            wrapMode: Text.NoWrap
            elide: Text.ElideRight

            anchors {
                left: parent.left
                leftMargin: 28
                top: camType.bottom
                topMargin: channelsData ? 4 : 6
            }

            text: {
                if (!streamData) return ""
                return streamData.camera.name + "  |  " + streamData.hub.name + " (ID " + streamData.hub.id + ")"
            }
        }

        Item {
            id: channelsItem
            height: scrollBar.policy == ScrollBar.AlwaysOn ? 32 : 28
            visible: channelsData
            anchors {
                left: parent.left
                leftMargin: 30
                right: control.left
                rightMargin: 30
                bottom: parent.bottom
                bottomMargin: 0
            }

            ScrollView {
                id: scrollView
                clip: true
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                    bottom: parent.bottom
                    bottomMargin: -10
                }

                ScrollBar.horizontal: ScrollBar {
                    id: scrollBar
                    policy: {
                        if (scrollView.width < channels.width) {
                            return ScrollBar.AlwaysOn
                        }
                        return ScrollBar.AlwaysOff
                    }
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10

                    contentItem: Rectangle {
                        implicitHeight: 2
                        implicitWidth: 100
                        radius: height / 2
                        color: scrollBar.pressed ? "#81e889" : "#9e9e9e"
                        opacity: 0.6
                    }

                    background: Rectangle {
                        implicitHeight: 2
                        implicitWidth: 100
                        color: "#575757"
                    }
                }

                Row {
                    id: channels
                    spacing: 22
                    height: parent.height

                    Repeater {
                        model: channelsData

                        Item {
                            width: 22
                            height: 22
                            enabled: channelSelected || player.state != "loading"

                            property var channelSelected: {
                                if (!channelsData) return false
                                return channelsData[index] == currentChannel
                            }

                            Text {
                                id: channelNo
                                color: channelSelected ? "#60e3ab" : "#fdfdfd"
                                opacity: {
                                    if (!parent.enabled) return 0.5
                                    return channelSelected ? 1 : 0.8
                                }
                                font.family: "Open Sans"
                                font.letterSpacing: 1
                                font.pixelSize: 14
                                font.bold: true
                                anchors {
                                    horizontalCenter: parent.horizontalCenter
                                    top: parent.top
                                }

                                text: channelsData[index]
                            }

                            Rectangle {
                                width: 4
                                height: width
                                radius: width/2
                                color: "#60e3ab"
                                visible: channelSelected
                                anchors {
                                    horizontalCenter: parent.horizontalCenter
                                    top: channelNo.bottom
                                    topMargin: 2
                                }
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (channelSelected) return
                                    currentChannel = channelNo.text
                                    player.change_dvr_channel(channelNo.text)
                                }
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            id: control
            color: "transparent"
            width: 140
            height: 46
            radius: height/2
            border.width: 2
            border.color: "#60e3ab"

            enabled: player.state != "error"
            opacity: enabled ? 1.0 : 0.6

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 28
            }

            Image {
                id: playImage
                source: player.state == "pause" ? "qrc:/resources/images/desktop/icons/ic-play-streamer.png" : "qrc:/resources/images/desktop/icons/ic-stop-streamer.png"
                sourceSize.width: 36
                sourceSize.height: 36
                anchors {
                    left: parent.left
                    leftMargin: 20
                    verticalCenter: parent.verticalCenter
                }

                MouseArea {
                    id: playArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (player.state == "pause") {
                            player.play()
                        } else {
                            player.pause()
                        }
                    }
                }
            }

            Rectangle {
                width: 2
                height: parent.height
                color: "#60e3ab"
                anchors {
                    top: parent.top
                    bottom: parent.bottom
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Image {
                id: snapshotImage
                source: "qrc:/resources/images/desktop/icons/ic-snapshot-streamer.png"
                sourceSize.width: 22
                sourceSize.height: 22
                anchors {
                    right: parent.right
                    rightMargin: 26
                    verticalCenter: parent.verticalCenter
                }

                MouseArea {
                    id: snapshotArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        player.snapshot()
                    }
                }
            }
        }
    }

    FileDialog {
        id: savePhotoFileDialog
        title: "Save snapshot"
        folder: shortcuts.home
        selectFolder: true
        selectExisting: false

        onAccepted: {
            player.save_snapshot(snapshotPath, fileUrl)
            savePhotoFileDialog.close()
        }
        onRejected: {
            savePhotoFileDialog.close()
        }
    }

    Connections {
        target: player

        onSnapshotTaken: {
            snapshotPath = value.path
            savePhotoFileDialog.open()
        }

        onPlayerDataReady: {
            streamData = value
        }

        onChannelsReady: {
            channelsData = value.channels
            currentChannel = value.currentChannel
        }

        onChannelsReset: {
            playerPanel.channelsData = null
            playerPanel.currentChannel = null
        }
    }
}
