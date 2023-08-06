import QtQuick 2.14
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/images.js" as Images


Item {
    id: carousel
//  To get selected photo outside the carousel
    property var selectedType: devicesModel[0]
//  To get selected color outside the carousel
    property alias colorPeaker: colorPeaker
//  Model of the devices
    property var devicesModel: ["CARD", "TAG"]

    width: parent.width
    height: 216

    ListView {
        id: view

        width: parent.width
        height: 128

        anchors {
            top: parent.top
            topMargin: 16
        }

        clip: true
        preferredHighlightBegin: width / 2 - 60
        preferredHighlightEnd: width / 2 + 60
        highlightRangeMode: ListView.StrictlyEnforceRange
        orientation: ListView.Horizontal
        flickableDirection: Flickable.HorizontalFlick
        model: devicesModel
        spacing: 8
        currentIndex: model.indexOf(selectedType)
        delegate: DS3.Image {
            width: 128
            height: 128

            source: Images.get_image(modelData, "Large", colorPeaker.currentColor)
            scale: view.currentIndex == index ? 1 : 0.7

            Behavior on scale {
                NumberAnimation {
                    duration: 200
                }
            }

            DS3.MouseArea {
                onClicked: {
                    view.currentIndex = index
                    carousel.selectedType = modelData
                }
            }
        }
    }

    DS3.Pagination {
        id: pagination

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: view.bottom
            topMargin: 16
        }

        amount: devicesModel.length
        current: view.currentIndex
    }

    DS3.ChipControlColor {
        id: colorPeaker

        anchors {
            horizontalCenter: parent.horizontalCenter
            top: pagination.bottom
            topMargin: 18
        }

        currentIndex: currentColor != "BLACK"
    }
}
