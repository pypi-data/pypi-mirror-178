import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom


GridView {
    id: photosGrid
    cellWidth: width / 3
    cellHeight: cellWidth * 0.75
    currentIndex: -1
    model: incident.motion_cam_events

    cacheBuffer: Math.ceil(model.length / 3) * cellHeight

    property var popupOpened: false

    signal changeImage()

    Timer {
        id: movieTimer
        interval: 500
        repeat: true
        running: true
        onTriggered: {
            photosGrid.changeImage()
        }
    }

    delegate: Item {
        id: delegGridItem
        width: photosGrid.cellWidth
        height: photosGrid.cellHeight

        property alias photoArea: photoArea

        property var trueEvent: event
        property var trueTimestamp: timestamp

        property var text: normal_text
        property var readyImages: ready_images
        property var dateTime: {
            var day = Date.fromLocaleString(application.locale, date, "yyyy-MM-dd")
            day = day.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.ShortFormat))
            return day + " " + time
        }
        property var dateTimeAlt: {
            var dt = new Date(timestamp * 1000)
            return dt.toLocaleString(application.locale, application.shortDateTimeFormat)
        }

        Item {
            id: deleg
            width: parent.width - 1
            height: parent.height - 1

            property var imageIndex: 0

            Connections {
                target: photosGrid

                onChangeImage: {
                    if (!photosGrid.visible) return
                    deleg.imageIndex = deleg.imageIndex == delegGridItem.readyImages.length - 1 ? 0 : deleg.imageIndex + 1
                }
            }

            Repeater {
                id: repeater
                model: delegGridItem.readyImages

                Image {
                    visible: index == deleg.imageIndex
                    source: modelData
                    asynchronous: true
                    anchors.fill: parent
                }
            }

            Rectangle {
                width: parent.width
                height: 28
                anchors.bottom: parent.bottom
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "transparent" }
                    GradientStop { position: 1.0; color: ui.colors.black }
                }

                Item {
                    width: 32
                    height: parent.height

                    Anime.GifPlayingIcon {
                        count: delegGridItem.readyImages.length
                        interval: movieTimer.interval
                        running: delegGridItem.readyImages.length > 1 && photosGrid.visible
                        currentIndex: deleg.imageIndex
                    }
                }

                Custom.FontText {
                    width: parent.width - 36
                    height: contentHeight
                    color: ui.colors.white
                    font.pixelSize: 14
                    maximumLineCount: 1
                    elide: Text.ElideRight
                    text: dateTime
                    anchors {
                        left: parent.left
                        leftMargin: 32
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Rectangle {
                color: "transparent"
                border.width: photosGrid.currentIndex == index ? 1 : 0
                border.color: ui.colors.green1
                anchors.fill: parent
            }

            Custom.HandMouseArea {
                id: photoArea
                onClicked: {
                    delegGridItem.readyImages = ready_images
                    photosGrid.currentIndex = index
                    if (photosGrid.popupOpened) return
                    photosGrid.popupOpened = true
                    Popups.motion_cam_popup(photosGrid, topLevel)
                }
            }
        }
    }
}