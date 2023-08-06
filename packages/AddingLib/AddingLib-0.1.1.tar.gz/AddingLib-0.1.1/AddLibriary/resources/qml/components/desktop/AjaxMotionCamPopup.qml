import QtQuick 2.7
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12
import QtQuick.Dialogs 1.3


AjaxPopup {
    id: popup
    width: popupBody.width
    height: popupBody.height

    property var data: null

    property var info: data == null ? null : data.information
    property var text_info: data == null ? null : data.text_info
    property var time: data == null ? null : data.time

    property var imageZoom: false
    property var imageIndex: 0

    Timer {
        id: gifTimer
        interval: 500
        repeat: true
        running: false
        onTriggered: {
            if (imageIndex != info.count - 1) {
                imageIndex += 1
            } else {
                imageIndex = 0
            }
        }
    }

    Rectangle {
        id: popupBody
        width: 400
        height: 400
        anchors.centerIn: parent
        color: "#252525"
        radius: 20
        focus: true

        Keys.onPressed: {
            if (event.key == Qt.Key_Left) {
                if (!leftArrow.visible || !leftArrow.enabled) return
                imageIndex = imageIndex - 1
                return
            }

            if (event.key == Qt.Key_Right) {
                if (!rightArrow.visible || !rightArrow.enabled) return
                imageIndex = imageIndex + 1
                return
            }
        }

        Item {
            id: headItem
            width: parent.width
            height: 50
            anchors.top: parent.top

            Item {
                id: minusItem
                width: 20
                height: 20
                opacity: imageZoom ? 1.0 : 0.3
                enabled: imageZoom
                anchors {
                    top: parent.top
                    topMargin: 15
                    left: parent.left
                    leftMargin: 15
                }

                Image {
                    source: "qrc:/resources/images/icons/ic-zoom-minus.png"
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            imageZoom = false
                            zoomMinusAnim.start()
                        }
                    }
                }
            }

            Item {
                id: plusItem
                width: 20
                height: 20
                opacity: imageZoom ? 0.3 : 1.0
                enabled: !imageZoom
                anchors {
                    top: parent.top
                    topMargin: 15
                    left: minusItem.right
                    leftMargin: info.count > 1 ? 64 : 92
                }

                Image {
                    source: "qrc:/resources/images/icons/ic-zoom-plus.png"
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            imageZoom = true
                            zoomPlusAnim.start()
                        }
                    }
                }
            }

            Item {
                id: playStopItem
                width: 20
                height: 20
                visible: info.count > 1
                anchors {
                    top: parent.top
                    topMargin: 15
                    horizontalCenter: parent.horizontalCenter
                }

                Image {
                    source: gifTimer.running ? "qrc:/resources/images/icons/ic-stop.png" : "qrc:/resources/images/icons/ic-play.png"
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (gifTimer.running) {
                                gifTimer.stop()
                            } else {
                                gifTimer.start()
                                imageIndex = 0
                            }
                        }
                    }
                }
            }

            Item {
                id: downloadItem
                width: 20
                height: 20
                anchors {
                    top: parent.top
                    topMargin: 15
                    right: closeItem.left
                    rightMargin: info.count > 1 ? 64 : 92
                }

                Image {
                    source: "qrc:/resources/images/icons/ic-download.png"
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            savePhotoFileDialog.open()
                        }
                    }
                }
            }

            Item {
                id: closeItem
                width: 20
                height: 20
                anchors {
                    top: parent.top
                    topMargin: 15
                    right: parent.right
                    rightMargin: 15
                }

                Image {
                    source: "qrc:/resources/images/icons/ic-close.png"
                    anchors.fill: parent

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            popup.close()
                        }
                    }
                }
            }
        }

        Item {
            id: bodyItem
            width: 400
            height: 300
            anchors.centerIn: parent

            Repeater {
                id: repeater
                model: info.count
                Image {
                    id: camImage
                    visible: index == imageIndex
                    source: info.photos[index].link
                    anchors.fill: parent
                }
            }

            Item {
                id: sliderPoints
                height: 20
                width: points.width
                visible: info.count > 1 && !gifTimer.running
                anchors {
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                }

                Row {
                    id: points
                    spacing: 12
                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        bottom: parent.bottom
                    }

                    Repeater {
                        model: info.count
                        Rectangle {
                            width: 10
                            height: 10
                            radius: width/2
                            color: index == imageIndex ? "#60e3ab" : "#252525"
                            opacity: 1

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    imageIndex = index
                                }
                            }
                        }
                    }
                }
            }
        }

        Item {
            id: tailItem
            width: parent.width
            height: 50
            anchors.bottom: parent.bottom

            Image {
                id: leftArrow
                width: 20
                height: 20
                visible: info.count > 1 && !gifTimer.running
                enabled: imageIndex != 0
                opacity: enabled ? 1 : 0.4
                source: "qrc:/resources/images/icons/ic-back-arrow.png"
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    leftMargin: 20
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        imageIndex = imageIndex - 1
                    }
                }
            }

            Image {
                id: rightArrow
                width: 20
                height: 20
                visible: info.count > 1 && !gifTimer.running
                enabled: imageIndex != info.count - 1
                opacity: enabled ? 1 : 0.4
                source: "qrc:/resources/images/icons/ic-arrow.png"
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    rightMargin: 20
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        imageIndex = imageIndex + 1
                    }
                }
            }

            Text {
                id: camInfo
                width: 280
                text: time + ", " + text_info
                color: "#a8aaab"
                font.family: roboto.name
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
            }
        }

        ParallelAnimation {
            id: zoomPlusAnim
            running: false
            PropertyAnimation { target: bodyItem; property: "width"; from: 400; to: 600;  duration: 200 }
            PropertyAnimation { target: bodyItem; property: "height"; from: 300; to: 450;  duration: 200 }
            PropertyAnimation { target: popupBody; property: "height"; from: 400; to: 550;  duration: 200 }
        }

        ParallelAnimation {
            id: zoomMinusAnim
            running: false
            PropertyAnimation { target: bodyItem; property: "width"; from: 600; to: 400;  duration: 200 }
            PropertyAnimation { target: bodyItem; property: "height"; from: 450; to: 300;  duration: 200 }
            PropertyAnimation { target: popupBody; property: "height"; from: 550; to: 400;  duration: 200 }
        }
    }

    FileDialog {
        id: savePhotoFileDialog
        title: gifTimer.running ? "Save gif" : "Save photo"
        folder: {
            var savedPath = client.get_save_path()
            return savedPath == "" ? shortcuts.home : savedPath
        }
        selectFolder: true
        onAccepted: {
            if (!gifTimer.running) {
                var photoIndex = imageIndex + 1
                var name = "MotionCam_" + info.device_id + "_" + info.full_time + "_" + photoIndex + ".jpg"
                client.save_motioncam_photo(info.photos[imageIndex].link, name, fileUrl)
            } else {
                var name = "MotionCam_" + info.device_id + "_" + info.full_time + ".gif"
                util.set_gif_info({"name": name, "file": fileUrl.toString(), "count": info.count})
                for (var i = 0; i < info.count; i++) {
                    repeater.itemAt(i).grabToImage(function(result) {
                        util.collect_image(result.image)
                    })
                }
            }
            savePhotoFileDialog.close()
        }
        onRejected: {
            savePhotoFileDialog.close()
        }
    }
}
