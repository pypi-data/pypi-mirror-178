import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup

    property var target: null
    property var url: null
    property var sideMargin: 24
    property var isRounded: true

    width: 500

    modal: false
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    onOpened: {
        if (trueImage.status == Image.Error) {
            target.imageData = {"x": 0, "y": 0, "w": 0, "h": 0, "url": url.toString()}
            popup.close()
        } else {
            popup.modal = true
            imageItem.visible = true
        }
    }

    header: DS3.NavBarModal {
        headerText: tr.Crop_selected_image_desktop

        onClosed: () => {
            popup.close()
        }
    }

    footer: DS3.ButtonBar {
        id: saveButton

        buttonText: tr.save
        hasBackground: true

        button.onClicked: {
            var xCoef = trueImage.width/objectImage.width
            var yCoef = trueImage.height/objectImage.height

            var x = selectedArea.x * xCoef
            var y = selectedArea.y * yCoef
            var w = selectedArea.width * xCoef
            var h = selectedArea.height * yCoef

            target.imageData = {"x": x, "y": y, "w": w, "h": h, "url": url.toString()}
            popup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Image {
        id: trueImage

        source: url
        visible: false
    }

    Item {
        id: imageItem

        property var coef: {
            if (!trueImage.width || !trueImage.height) return 1
            if (trueImage.width >= trueImage.height) {
                return 400 / trueImage.width
            } else {
                return 500 / trueImage.height
            }
        }

        width: objectImage.width
        height: objectImage.height

        anchors.horizontalCenter: parent.horizontalCenter

        Image {
            id: objectImage

            width: trueImage.width * imageItem.coef
            height: trueImage.height * imageItem.coef

            anchors.centerIn: parent

            source: url
        }

        Rectangle {
            id: selectedArea

            width: Math.min(objectImage.width, objectImage.height)
            height: width

            color: ui.ds3.figure.transparent
            radius: width / 2
            x: (objectImage.width - width) / 2
            y: (objectImage.height - height) / 2

            DS3.MouseArea {
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
            id: maskCircle

            anchors.fill: parent

            visible: false
            color: ui.ds3.figure.transparent

            Rectangle {
                width: selectedArea.width
                height: selectedArea.height

                x: selectedArea.x
                y: selectedArea.y
                radius: isRounded ? width / 2 : 0
            }
        }

        Rectangle {
            anchors.fill: parent

            color: ui.ds3.bg.low
            opacity: 0.7

            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: maskCircle
                invert: true
            }
        }

        Rectangle {
            width: 10
            height: 10

            anchors {
                verticalCenter: selectedArea.top
                horizontalCenter: selectedArea.left
            }

            color: ui.ds3.figure.contrast
            opacity: 0.7

            MouseArea {
                anchors.fill: parent

                cursorShape: Qt.SizeFDiagCursor

                onPositionChanged: {
                    var minX = selectedArea.x - Math.min(selectedArea.x, selectedArea.y)
                    var minY = selectedArea.y - Math.min(selectedArea.x, selectedArea.y)
                    var maxX = selectedArea.x + selectedArea.width - 30
                    var maxY = selectedArea.y + selectedArea.height - 30

                    if (mouseX*mouseY > 0) {
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

            anchors {
                verticalCenter: selectedArea.top
                horizontalCenter: selectedArea.right
            }

            color: ui.ds3.figure.contrast
            opacity: 0.7

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

            anchors {
                verticalCenter: selectedArea.bottom
                horizontalCenter: selectedArea.left
            }

            color: ui.ds3.figure.contrast
            opacity: 0.7

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

            anchors {
                verticalCenter: selectedArea.bottom
                horizontalCenter: selectedArea.right
            }

            color: ui.ds3.figure.contrast
            opacity: 0.7

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

    DS3.Spacing {
        height: 24
    }
}
