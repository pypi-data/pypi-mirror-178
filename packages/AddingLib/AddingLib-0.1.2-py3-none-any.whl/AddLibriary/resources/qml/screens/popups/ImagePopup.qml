import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom



AjaxPopup {
    id: popup

    width: imageItem.width
    height: header.height + imageItem.height + saveCancelArea.height

    modal: true
    focus: true
    objectName: "imagePopup"
    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    anchors.centerIn: parent

    property var target: null
    property var url: null

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    Image {
        id: trueImage

        source: url
        visible: false
    }

    contentItem: Rectangle {
        id: bodyRect

        radius: 10
        focus: true
        color: ui.colors.dark3

        anchors.fill: parent

        Custom.PopupHeader {
            id: header

            width: parent.width
            height: 64
            zoneHeight: height
            radius: parent.radius

            title: tr.Crop_selected_image_desktop

            anchors.top: parent.top
            headerTitle.anchors.leftMargin: 32

            closeArea.onClicked: {
                popup.close()
            }
        }

        Item {
            id: imageItem

            width: objectImage.width
            height: objectImage.height

            anchors {
                top: header.bottom
                horizontalCenter: parent.horizontalCenter
            }

            property var k: {
                if (!trueImage.width || !trueImage.height) return 1
                if (trueImage.width >= trueImage.height) {
                    return 400 / trueImage.width
                } else {
                    return 500 / trueImage.height
                }
            }

            Image {
                id: objectImage

                source: popup.url
                anchors.centerIn: parent

                width: {
                    var imageWidth = trueImage.width * imageItem.k
                    if (imageWidth > 400) return 400
                    if (imageWidth < 250) return 250
                    return imageWidth
                }

                height: {
                    var imageHeight = trueImage.height * imageItem.k
                    if (imageHeight > 500) return 500
                    if (imageHeight < 250) return 250
                    return imageHeight
                }
            }

            Rectangle {
                id: selectedArea

                width: 150
                height: 150

                color: "transparent"

                x: (objectImage.width - width) / 2
                y: (objectImage.height - height) / 2

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.DragMoveCursor

                    drag {
                        target: selectedArea
                        axis: Drag.XAndYAxis
                        minimumX: 0
                        minimumY: 0
                        maximumX: objectImage.width - selectedArea.width
                        maximumY: objectImage.height - selectedArea.height
                    }
                }
            }

            Rectangle {
                color: ui.colors.dark4
                opacity: 0.5

                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                    bottom: selectedArea.top
                }
            }

            Rectangle {
                color: ui.colors.dark4
                opacity: 0.5

                anchors {
                    top: selectedArea.bottom
                    left: parent.left
                    right: parent.right
                    bottom: parent.bottom
                }
            }

            Rectangle {
                color: ui.colors.dark4
                opacity: 0.5

                anchors {
                    top: selectedArea.top
                    left: parent.left
                    right: selectedArea.left
                    bottom: selectedArea.bottom
                }
            }

            Rectangle {
                color: ui.colors.dark4
                opacity: 0.5

                anchors {
                    top: selectedArea.top
                    left: selectedArea.right
                    right: parent.right
                    bottom: selectedArea.bottom
                }
            }

            Rectangle {
                width: 10
                height: 10

                color: ui.colors.light1
                opacity: 0.7

                anchors {
                    verticalCenter: selectedArea.top
                    horizontalCenter: selectedArea.left
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.SizeFDiagCursor

                    onPositionChanged: {
                        var minX = selectedArea.x - Math.min(selectedArea.x, selectedArea.y)
                        var minY = selectedArea.y - Math.min(selectedArea.x, selectedArea.y)
                        var maxX = selectedArea.x + selectedArea.width - 30
                        var maxY = selectedArea.y + selectedArea.height - 30

                        if (mouseX * mouseY > 0) {
                            var coordMin = Math.min(Math.abs(mouseX), Math.abs(mouseY)) * (mouseX / Math.abs(mouseX))

                            if (selectedArea.x + coordMin > minX && selectedArea.x + coordMin < maxX && selectedArea.y + coordMin > minY && selectedArea.y + coordMin < maxY) {
                                selectedArea.x += coordMin
                                selectedArea.y += coordMin

                                selectedArea.width -= coordMin
                                selectedArea.height -= coordMin
                            }
                        }
                    }
                }
            }

            Rectangle {
                width: 10
                height: 10

                color: ui.colors.light1
                opacity: 0.7

                anchors {
                    verticalCenter: selectedArea.top
                    horizontalCenter: selectedArea.right
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.SizeBDiagCursor

                    onPositionChanged: {
                        var startPosX = selectedArea.x

                        var minX = selectedArea.x + 30
                        var minY = selectedArea.y - Math.min(objectImage.width - selectedArea.x - selectedArea.width, selectedArea.y)
                        var maxX = selectedArea.x + Math.min(objectImage.width - selectedArea.x - selectedArea.width, selectedArea.y)
                        var maxY = selectedArea.y + selectedArea.height - 30

                        if (mouseX*mouseY < 0) {
                            var coordMin = Math.min(Math.abs(mouseX), Math.abs(mouseY)) * (mouseX / Math.abs(mouseX))

                            if (selectedArea.x + selectedArea.width + coordMin > minX && selectedArea.x + coordMin < maxX && selectedArea.y - coordMin > minY && selectedArea.y - coordMin < maxY) {
                                selectedArea.x = startPosX
                                selectedArea.y -= coordMin

                                selectedArea.width += coordMin
                                selectedArea.height += coordMin
                            }
                        }
                    }
                }
            }

            Rectangle {
                width: 10
                height: 10

                color: ui.colors.light1
                opacity: 0.7

                anchors {
                    verticalCenter: selectedArea.bottom
                    horizontalCenter: selectedArea.left
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.SizeBDiagCursor

                    onPositionChanged: {
                        var startPosY = selectedArea.y

                        var minX = selectedArea.x - Math.min(selectedArea.x, objectImage.height - selectedArea.y - selectedArea.height)
                        var minY = selectedArea.y + 30
                        var maxX = selectedArea.x + selectedArea.width - 30
                        var maxY = selectedArea.y + selectedArea.height + Math.min(selectedArea.x, objectImage.height - selectedArea.y - selectedArea.height)

                        if (mouseX*mouseY < 0) {
                            var coordMin = Math.min(Math.abs(mouseX), Math.abs(mouseY)) * (mouseY / Math.abs(mouseY))

                            if (selectedArea.x - coordMin > minX && selectedArea.x - coordMin < maxX && selectedArea.y + selectedArea.height + coordMin > minY && selectedArea.y + coordMin < maxY) {
                                selectedArea.x -= coordMin
                                selectedArea.y = startPosY

                                selectedArea.width += coordMin
                                selectedArea.height += coordMin
                            }
                        }
                    }
                }
            }

            Rectangle {
                width: 10
                height: 10

                color: ui.colors.light1
                opacity: 0.7

                anchors {
                    verticalCenter: selectedArea.bottom
                    horizontalCenter: selectedArea.right
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.SizeFDiagCursor

                    onPositionChanged: {
                        var startPosX = selectedArea.x
                        var startPosY = selectedArea.y

                        var minX = selectedArea.x + 30
                        var minY = selectedArea.y + 30
                        var maxX = selectedArea.x + selectedArea.width + Math.min(objectImage.width - selectedArea.x - selectedArea.width, objectImage.height - selectedArea.y - selectedArea.height)
                        var maxY = selectedArea.y + selectedArea.height + Math.min(objectImage.width - selectedArea.x - selectedArea.width, objectImage.height - selectedArea.y - selectedArea.height)

                        if (mouseX*mouseY > 0) {
                            var coordMin = Math.min(Math.abs(mouseX), Math.abs(mouseY)) * (mouseX / Math.abs(mouseX))

                            if (selectedArea.x + selectedArea.width + coordMin > minX && selectedArea.x + selectedArea.width + coordMin < maxX && selectedArea.y + selectedArea.height + coordMin > minY && selectedArea.y + selectedArea.height + coordMin < maxY) {
                                selectedArea.x = startPosX
                                selectedArea.y = startPosY

                                selectedArea.width += coordMin
                                selectedArea.height += coordMin
                            }
                        }
                    }
                }
            }
        }

        Item {
            id: saveCancelArea

            width: parent.width
            height: 80

            anchors {
                top: imageItem.bottom
                horizontalCenter: parent.horizontalCenter
            }

        }

        /*
        AjaxSaveCancel {
            id: saveCancelArea
            anchors.bottom: parent.bottom

            cancelArea.onClicked: {
                popup.close()
            }

            saveArea.onClicked: {
                var xKoef = trueImage.width/objectImage.width
                var yKoef = trueImage.height/objectImage.height

                var x = selectedArea.x * xKoef
                var y = selectedArea.y * yKoef
                var w = selectedArea.width * xKoef
                var h = selectedArea.height * yKoef

                target.imageData = {"x": x, "y": y, "w": w, "h": h, "url": url.toString()}
                popup.close()
            }
        }
        */
    }
}
