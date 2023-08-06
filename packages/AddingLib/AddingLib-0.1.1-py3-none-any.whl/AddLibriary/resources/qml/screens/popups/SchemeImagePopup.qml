import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.3

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "schemePopup"
    width: 400
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

    property var imageZoom: false
    property var imageZoomAdditional: false
    property var normalXY: [0, 0]
    property var margin: width / 3 + 3
    property var currentGridItem: grid.itemAtIndex(grid.currentIndex)

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

            Image {
                id: originalImage
                fillMode: Image.PreserveAspectFit
                source: popup.currentGridItem ? currentGridItem.schemeUrl["original"] : ""
                anchors.fill: parent
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
                        if (grid.currentIndex == 0) {
                            grid.currentIndex = grid.model.length - 1
                        } else {
                            grid.currentIndex -= 1
                        }
                    }
                }
            }

            Custom.FontText {
                id: captionText
                width: parent.width - 128
                height: contentHeight
                color: ui.colors.white
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
                text: popup.currentGridItem ? popup.currentGridItem.schemeCaption : ""
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
                        if (grid.currentIndex == grid.model.length - 1) {
                            grid.currentIndex = 0
                        } else {
                            grid.currentIndex += 1
                        }
                    }
                }
            }
        }

        ParallelAnimation {
            id: zoomPlusAnim
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; from: 400; to: 600;  duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; from: 300; to: 450;  duration: 200 }
            PropertyAnimation { target: backRect; property: "opacity"; to: 0.6;  duration: 200 }

            PropertyAnimation { target: popup; property: "width"; from: 400; to: 600;  duration: 200 }
            PropertyAnimation { target: popup; property: "height"; from: 400; to: 550;  duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: (application.width - 600) / 2;  duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: (application.height - 550) / 2;  duration: 200 }
        }

        ParallelAnimation {
            id: zoomPlusAnimAdditional
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; from: 600; to: 720;  duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; from: 450; to: 540;  duration: 200 }

            PropertyAnimation { target: popup; property: "width"; from: 600; to: 720;  duration: 200 }
            PropertyAnimation { target: popup; property: "height"; from: 550; to: 640;  duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: (application.width - 720) / 2;  duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: (application.height - 640) / 2;  duration: 200 }
        }

        ParallelAnimation {
            id: zoomMinusAnim
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; from: 600; to: 400;  duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; from: 450; to: 300;  duration: 200 }
            PropertyAnimation { target: backRect; property: "opacity"; to: 0.0;  duration: 200 }

            PropertyAnimation { target: popup; property: "width"; from: 600; to: 400;  duration: 200 }
            PropertyAnimation { target: popup; property: "height"; from: 550; to: 400;  duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: popup.checkCoordinates()[0];  duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: popup.checkCoordinates()[1];  duration: 200 }
        }

        ParallelAnimation {
            id: zoomMinusAnimAdditional
            running: false

            PropertyAnimation { target: bodyImage; property: "width"; from: 720; to: 600;  duration: 200 }
            PropertyAnimation { target: bodyImage; property: "height"; from: 540; to: 450;  duration: 200 }

            PropertyAnimation { target: popup; property: "width"; from: 720; to: 600;  duration: 200 }
            PropertyAnimation { target: popup; property: "height"; from: 640; to: 550;  duration: 200 }
            PropertyAnimation { target: popup; property: "x"; to: (application.width - 600) / 2;  duration: 200 }
            PropertyAnimation { target: popup; property: "y"; to: (application.height - 550) / 2;  duration: 200 }
        }
    }

    Component.onDestruction: {
        grid.popupOpened = false
        grid.currentIndex = -1
    }

    Connections {
        target: grid

        onCurrentIndexChanged: {
            if (grid.currentIndex == -1) popup.destroy()
        }
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
        title: captionText.text ? tr.save_photo + "  (" + captionText.text + ")" : tr.save_photo

        onRejected: {
            savePhotoFileDialog.close()
        }

        onAccepted: {
            var name = captionText.text ? captionText.text + ".png" : "plan.png"

            util.set_gif_info({"name": name, "file": fileUrl.toString(), "count": 1})
            originalImage.grabToImage(function(result) {
                util.collect_image(result.image)
            })

            savePhotoFileDialog.close()
        }
    }
}