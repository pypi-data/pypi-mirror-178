import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.3

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "facilityMotionCamPopup"
    implicitWidth: 400
    implicitHeight: 400
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true

    anchors.centerIn: parent

    property var event: null

    property var imageZoom: false
    property var imageZoomAdditional: false
    property var margin: width / 4 + 10

    property var scaleFactor: 4 / 3

    signal prevImage()
    signal nextImage()

    onPrevImage: {
        bodyItem.imageIndex = bodyItem.imageIndex == 0 ? repeater.model.length - 1 : bodyItem.imageIndex - 1
    }

    onNextImage: {
        bodyItem.imageIndex = bodyItem.imageIndex == repeater.model.length - 1 ? 0 : bodyItem.imageIndex + 1
    }


    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y

    }

    Timer {
        id: movieTimer
        interval: 500
        repeat: true
        running: true
        onTriggered: {
            nextImage()
        }
    }

    Rectangle {
        radius: 16
        color: ui.colors.dark2
        anchors.fill: parent

        Item {
            id: headItem
            width: parent.width
            height: 50
            anchors.top: parent.top

            Item {
                width: 24
                height: 24
                enabled: imageZoom
                opacity: enabled ? 1 : 0.5
                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/zoom-out.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        if (imageZoomAdditional) {
                            imageZoomAdditional = false
                            zoomMinusAnimAdditional.start()
                            return
                        }

                        if (imageZoom) {
                            imageZoom = false
                            zoomMinusAnim.start()
                            return
                        }
                    }
                }
            }

            Item {
                width: 24
                height: 24
                enabled: !imageZoomAdditional
                opacity: enabled ? 1 : 0.5
                anchors {
                    left: parent.left
                    leftMargin: popup.margin
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/zoom-in.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        if (!imageZoom) {
                            imageZoom = true
                            zoomPlusAnim.start()
                            return
                        }

                        if (!imageZoomAdditional) {
                            imageZoomAdditional = true
                            zoomPlusAnimAdditional.start()
                            return
                        }
                    }
                }
            }

            Item {
                width: 24
                height: 24
                anchors {
                    centerIn: parent
                }

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    anchors.centerIn: parent
                    source: movieTimer.running ? "qrc:/resources/images/icons/pause.svg" : "qrc:/resources/images/icons/play.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        movieTimer.running = !movieTimer.running
                    }
                }
            }

            Item {
                width: 24
                height: 24
                enabled: true
                opacity: enabled ? 1 : 0.5
                anchors {
                    right: parent.right
                    rightMargin: popup.margin
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/download.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        savePhotoFileDialog.open()
                    }
                }
            }

            Item {
                width: 24
                height: 24
                anchors {
                    right: parent.right
                    rightMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/window-close.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        popup.close()
                    }
                }
            }
        }

        Item {
            id: bodyItem
            clip: true
            implicitWidth: popup.implicitWidth
            implicitHeight: popup.implicitHeight - 100
            anchors.centerIn: parent

            property var imageIndex: 0

            Repeater {
                id: repeater
                model: popup.event.ready_images

                Image {
                    visible: index == bodyItem.imageIndex
                    source: modelData
                    asynchronous: true
                    anchors.fill: parent
                }
            }

            Item {
                id: sliderPoints
                height: 20
                width: points.width
                visible: repeater.model.length > 1 && !movieTimer.running
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
                        model: repeater.model.length

                        Rectangle {
                            width: 10
                            height: width
                            radius: width/2
                            color: index == bodyItem.imageIndex ? ui.colors.green1 : ui.colors.dark4
                        }
                    }
                }
            }
        }

        Item {
            id: bottomItem
            width: parent.width
            height: 50
            anchors.bottom: parent.bottom

            Item {
                width: 40
                height: 40
                visible: !movieTimer.running
                anchors {
                    left: parent.left
                    leftMargin: 20
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 40
                    sourceSize.height: 40
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/a-left.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        prevImage()
                    }
                }
            }

            Custom.FontText {
                width: movieTimer.running ? parent.width - 64 : parent.width - 128
                height: contentHeight
                color: ui.colors.white
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
                text: {
                    var dt = new Date(popup.event.timestamp * 1000)
                    return dt.toLocaleString(application.locale, application.shortDateTimeFormat) + ", " + popup.event.notif_text
                }
            }

            Item {
                width: 40
                height: 40
                visible: !movieTimer.running
                anchors {
                    right: parent.right
                    rightMargin: 20
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 40
                    sourceSize.height: 40
                    rotation: 180
                    anchors.centerIn: parent
                    source: "qrc:/resources/images/icons/a-left.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        nextImage()
                    }
                }
            }
        }

        ParallelAnimation {
            id: zoomPlusAnim
            running: false

            PropertyAnimation {
                target: bodyItem;
                property: "width";
                from: bodyItem.implicitWidth;
                to: bodyItem.implicitWidth * popup.scaleFactor;
                duration: 200
            }
            PropertyAnimation {
                target: bodyItem;
                property: "height";
                from: bodyItem.implicitHeight;
                to: bodyItem.implicitHeight * popup.scaleFactor;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "width";
                from: popup.implicitWidth;
                to: popup.implicitWidth * popup.scaleFactor;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "height";
                from: popup.implicitHeight;
                to: popup.implicitHeight * popup.scaleFactor;
                duration: 200
            }
        }

        ParallelAnimation {
            id: zoomPlusAnimAdditional
            running: false

            PropertyAnimation {
                target: bodyItem;
                property: "width";
                from: bodyItem.implicitWidth * popup.scaleFactor;
                to: bodyItem.implicitWidth * popup.scaleFactor ** 2;
                duration: 200
            }
            PropertyAnimation {
                target: bodyItem;
                property: "height";
                from: bodyItem.implicitHeight * popup.scaleFactor;
                to: bodyItem.implicitHeight * popup.scaleFactor ** 2;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "width";
                from: popup.implicitWidth * popup.scaleFactor;
                to: popup.implicitWidth * popup.scaleFactor ** 2;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "height";
                from: popup.implicitHeight * popup.scaleFactor;
                to: popup.implicitHeight * popup.scaleFactor ** 2;
                duration: 200
            }
        }

        ParallelAnimation {
            id: zoomMinusAnim
            running: false

            PropertyAnimation {
                target: bodyItem;
                property: "width";
                from: bodyItem.implicitWidth * popup.scaleFactor;
                to: bodyItem.implicitWidth;
                duration: 200
            }
            PropertyAnimation {
                target: bodyItem;
                property: "height";
                from: bodyItem.implicitHeight * popup.scaleFactor;
                to: bodyItem.implicitHeight;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "width";
                from: popup.implicitWidth * popup.scaleFactor;
                to: popup.implicitWidth;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "height";
                from: popup.implicitHeight * popup.scaleFactor;
                to: popup.implicitHeight;
                duration: 200
            }
        }

        ParallelAnimation {
            id: zoomMinusAnimAdditional
            running: false

            PropertyAnimation {
                target: bodyItem;
                property: "width";
                from: bodyItem.implicitWidth * popup.scaleFactor ** 2;
                to: bodyItem.implicitWidth * popup.scaleFactor;
                duration: 200
            }
            PropertyAnimation {
                target: bodyItem;
                property: "height";
                from: bodyItem.implicitHeight * popup.scaleFactor ** 2;
                to: bodyItem.implicitHeight * popup.scaleFactor;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "width";
                from: popup.implicitWidth * popup.scaleFactor ** 2;
                to: popup.implicitWidth * popup.scaleFactor;
                duration: 200
            }
            PropertyAnimation {
                target: popup;
                property: "height";
                from: popup.implicitHeight * popup.scaleFactor ** 2;
                to: popup.implicitHeight * popup.scaleFactor;
                duration: 200
            }
        }
    }

    FileDialog {
        id: savePhotoFileDialog
        selectFolder: true
        folder: shortcuts.home
        title: movieTimer.running ? tr.save_as_video : tr.save_photo

        onRejected: {
            savePhotoFileDialog.close()
        }

        onAccepted: {
            var dt = new Date(popup.event.timestamp * 1000)
            var name = popup.event.event.hub_event.source_type == "18" ? "MotionCamOutdoor_" : "MotionCam_"
            name += popup.event.event.hub_event.source_id + "_" + dt.toLocaleString(application.locale, "yyyy-MM-dd_hh-mm-ss")
            name += movieTimer.running ? ".gif" : "_" + (bodyItem.imageIndex + 1) + ".jpg"

            var count = movieTimer.running ? repeater.model.length : 1

            util.set_gif_info({"name": name, "file": fileUrl.toString(), "count": count})

            if (movieTimer.running) {
                for (var i = 0; i < repeater.model.length; i++) {
                    repeater.itemAt(i).grabToImage(function(result) {
                        util.collect_image(result.image)
                    })
                }
            } else {
                /*
                repeater.itemAt(bodyItem.imageIndex).grabToImage(function(result) {
                    util.collect_image(result.image)
                })
                */

                app.save_photo(popup.event.ready_images[bodyItem.imageIndex], name, fileUrl)
            }

            savePhotoFileDialog.close()
        }
    }
}