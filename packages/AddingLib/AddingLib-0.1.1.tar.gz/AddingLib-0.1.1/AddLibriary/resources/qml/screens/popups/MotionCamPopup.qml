import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.3

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "motionCamPopup"
    width: bodyImage.width
    height: 400
    modal: false
    closePolicy: Popup.NoAutoClose

    x: (application.width - width) / 2
    y: (application.height - height) / 2

    destructOnClose: false

    anchors.centerIn: null
    parent: ApplicationWindow.contentItem

    visible: incidentPage.visible

    function checkCoordinates() {
        var trueX = normalXY[0]
        var trueY = normalXY[1]

        if (trueX < 0) trueX = 0
        if (trueY < 0) trueY = 0
        if (trueX > application.width - 400) {
            trueX = application.width - 400
        }
        if (trueY > application.height - 400) {
            trueY = application.height - 400
        }

        return [trueX, trueY]
    }

    property var grid: null
    property var incidentPage: null

    property var playing: true
    property var imageZoom: false
    property var imageZoomAdditional: false
    property var normalXY: [0, 0]
    property var margin: width / 4 + 10
    property var scaleFactor: 4 / 3

    onImageZoomChanged: {
        if (imageZoom) {
            popup.normalXY = [popup.x, popup.y]
            popup.modal = true
        } else {
            popup.modal = false
        }
    }

    background: Rectangle {
        id: backRect
        color: "black"
        opacity: 0.0
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
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

            Custom.HandMouseArea {
                property var clickPosition: null
                pressAndHoldInterval: 300
                enabled: !imageZoom

                onPressAndHold: {
                    popup.opacity = 0.7
                }

                onReleased: {
                    popup.opacity = 1.0
                }

                onPressed: {
                    clickPosition = Qt.point(mouseX, mouseY)
                }

                onPositionChanged: {
                    if (pressed) {
                        mouse.accepted = false
                        popup.x += mouseX - clickPosition.x
                        popup.y += mouseY - clickPosition.y
                        if (popup.x < 0) popup.x = 0
                        if (popup.y < 0) popup.y = 0
                        if (popup.x > application.width - popup.width) {
                            popup.x = application.width - popup.width
                        }
                        if (popup.y > application.height - popup.height) {
                            popup.y = application.height - popup.height
                        }
                    }
                }
            }

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
                    source: popup.playing ? "qrc:/resources/images/icons/pause.svg" : "qrc:/resources/images/icons/play.svg"
                }

                Custom.HandMouseArea {
                    onClicked: {
                        popup.playing = !popup.playing
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
                        popup.destroy()
                    }
                }
            }
        }

        Item {
            id: bodyImage
            width: 400
            height: 300
            anchors.centerIn: parent

            property var imageIndex: 0

            Connections {
                target: grid

                onChangeImage: {
                    if (!popup.playing) return
                    bodyImage.imageIndex = bodyImage.imageIndex == repeater.model.length - 1 ? 0 : bodyImage.imageIndex + 1
                }

                onCurrentIndexChanged: {
                    bodyImage.imageIndex = 0
                }
            }

            Repeater {
                id: repeater
                model: {
                    var item = grid.itemAtIndex(grid.currentIndex)
                    return item ? item.readyImages : []
                }

                Image {
                    visible: index == bodyImage.imageIndex
                    source: modelData
                    asynchronous: true
                    anchors.fill: parent

                    onStatusChanged: {
                        if (status == Image.Ready) {
                            // MCO
                            if (Math.abs(sourceSize.width / sourceSize.height - 20 / 11) < Number.EPSILON && bodyImage.width != 545) {
                                bodyImage.width = 545
                            }
                            // MC
                            else if (Math.abs(sourceSize.width / sourceSize.height - 4 / 3) < Number.EPSILON && bodyImage.width != 400) {
                                bodyImage.width = 400
                            }
                        }
                    }
                }
            }

            Item {
                id: sliderPoints
                height: 20
                width: points.width
                visible: repeater.model.length > 1 && !popup.playing
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
                            color: index == bodyImage.imageIndex ? ui.colors.green1 : ui.colors.dark4
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
                        if (popup.playing) {
                            if (grid.currentIndex == 0) {
                                grid.currentIndex = grid.model.length - 1
                            } else {
                                grid.currentIndex -= 1
                            }
                        } else {
                            if (bodyImage.imageIndex == 0) {
                                if (grid.currentIndex == 0) {
                                    grid.currentIndex = grid.model.length - 1
                                } else {
                                    grid.currentIndex -= 1
                                }
                            } else {
                                bodyImage.imageIndex -= 1
                            }
                        }
                    }
                }
            }

            Custom.FontText {
                width: parent.width - 128
                height: contentHeight
                color: ui.colors.white
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
                text: {
                    var item = grid.itemAtIndex(grid.currentIndex)
                    return item ? item.dateTimeAlt + ", " + item.text : ""
                }
            }

            Item {
                width: 40
                height: 40
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
                        if (popup.playing) {
                            if (grid.currentIndex == grid.model.length - 1) {
                                grid.currentIndex = 0
                            } else {
                                grid.currentIndex += 1
                            }
                        } else {
                            if (bodyImage.imageIndex == repeater.model.length - 1) {
                                if (grid.currentIndex == grid.model.length - 1) {
                                    grid.currentIndex = 0
                                } else {
                                    grid.currentIndex += 1
                                }
                            } else {
                                bodyImage.imageIndex += 1
                            }
                        }
                    }
                }
            }
        }

        ParallelAnimation {
            id: zoomPlusAnim
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; to: bodyImage.width * scaleFactor; duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; to: bodyImage.height * scaleFactor; duration: 200 }
            PropertyAnimation { target: backRect; property: "opacity"; to: 0.6;  duration: 200 }

            PropertyAnimation { target: popup; property: "width"; to: bodyImage.width * scaleFactor; duration: 200 }
            PropertyAnimation { target: popup; property: "height"; to: bodyImage.height * scaleFactor + 100; duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: (application.width - bodyImage.width * scaleFactor) / 2; duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: (application.height - bodyImage.height * scaleFactor - 100) / 2; duration: 200 }
        }

        ParallelAnimation {
            id: zoomPlusAnimAdditional
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; to: bodyImage.width * scaleFactor; duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; to: bodyImage.height * scaleFactor; duration: 200 }

            PropertyAnimation { target: popup; property: "width"; to: bodyImage.width * scaleFactor; duration: 200 }
            PropertyAnimation { target: popup; property: "height"; to: bodyImage.height * scaleFactor + 100; duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: (application.width - bodyImage.width * scaleFactor) / 2; duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: (application.height - bodyImage.height * scaleFactor - 100) / 2; duration: 200 }
        }

        ParallelAnimation {
            id: zoomMinusAnim
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; to: bodyImage.width / scaleFactor; duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; to: bodyImage.height / scaleFactor; duration: 200 }
            PropertyAnimation { target: backRect; property: "opacity"; to: 0.0;  duration: 200 }

            PropertyAnimation { target: popup; property: "width"; to: bodyImage.width / scaleFactor; duration: 200 }
            PropertyAnimation { target: popup; property: "height"; to: bodyImage.height / scaleFactor + 100; duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: popup.checkCoordinates()[0]; duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: popup.checkCoordinates()[1]; duration: 200 }
        }

        ParallelAnimation {
            id: zoomMinusAnimAdditional
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; to: bodyImage.width / scaleFactor; duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; to: bodyImage.height / scaleFactor; duration: 200 }

            PropertyAnimation { target: popup; property: "width"; to: bodyImage.width / scaleFactor; duration: 200 }
            PropertyAnimation { target: popup; property: "height"; to: bodyImage.height / scaleFactor + 100; duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: (application.width - bodyImage.width / scaleFactor) / 2; duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: (application.height - bodyImage.height / scaleFactor - 100) / 2; duration: 200 }
        }
    }

    Component.onDestruction: {
        grid.popupOpened = false
        grid.currentIndex = -1
    }

    Connections {
        target: application

        onWidthChanged: {
            if (popup.x + popup.width > application.width) {
                popup.x = application.width - popup.width
            }

            if (popup.imageZoom) popup.x = (application.width - popup.width) / 2
        }

        onHeightChanged: {
            if (popup.y + popup.height > application.height) {
                popup.y = application.height - popup.height
            }

            if (popup.imageZoom) popup.y = (application.height - popup.height) / 2
        }
    }

    FileDialog {
        id: savePhotoFileDialog
        selectFolder: true
        folder: shortcuts.home
        title: popup.playing ? tr.save_as_video : tr.save_photo

        onRejected: {
            savePhotoFileDialog.close()
        }

        onAccepted: {
            var event = grid.itemAtIndex(grid.currentIndex).trueEvent

            var dt = new Date(grid.itemAtIndex(grid.currentIndex).trueTimestamp * 1000)
            var name = event.hub_event.source_type == "18" ? "MotionCamOutdoor_" : "MotionCam_"
            name += event.hub_event.source_id + "_" + dt.toLocaleString(application.locale, "yyyy-MM-dd_hh-mm-ss")
            name += popup.playing ? ".gif" : "_" + (bodyImage.imageIndex + 1) + ".jpg"

            var count = popup.playing ? repeater.model.length : 1

            util.set_gif_info({"name": name, "file": fileUrl.toString(), "count": count})

            if (popup.playing) {
                for (var i = 0; i < repeater.model.length; i++) {
                    repeater.itemAt(i).grabToImage(function(result) {
                        util.collect_image(result.image)
                    })
                }
            } else {
                /*
                repeater.itemAt(bodyImage.imageIndex).grabToImage(function(result) {
                    util.collect_image(result.image)
                })
                */

                app.save_photo(repeater.model[bodyImage.imageIndex], name, fileUrl)
            }

            savePhotoFileDialog.close()
        }
    }
}