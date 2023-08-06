import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    id: settingsPicker

    property alias backgroundColor: backgroundRectangle.color

    delegate: ItemDelegate {
        id: itemDelegate

        width: settingsPicker.width
        height: 40

        padding: 0

        contentItem: Rectangle {
            width: settingsPicker.width
            height: 40

            color: settingsPicker.highlightedIndex == index ? ui.ds3.bg.high : ui.ds3.bg.highest

            DS3.Image {
                id: delegateImage

                width: 24
                height: 24

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    leftMargin: 16
                }

                source: modelData.image
            }

            DS3.Text {
                width: parent.width - 64

                anchors {
                    verticalCenter: parent.verticalCenter
                    left: delegateImage.right
                    leftMargin: 16
                }

                style: ui.ds3.text.body.MRegular
                text: modelData.text
                hasElide: true
                rightPadding: 30
            }

            DS3.Icon {
                anchors {
                    right: parent.right
                    rightMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                visible: settingsPicker.currentIndex == index
                source: "qrc:/resources/images/Athena/common_icons/Shape.svg"
            }
        }
    }

    contentItem: Item {
        height: atomTitle.height + 24

        anchors {
            left: parent.left
            right: indicator.left
            margins: 16
        }

        DS3.Image {
            id: delegateImage

            width: 24
            height: 24

            anchors.verticalCenter: parent.verticalCenter
            source: settingsPicker.model.length ? settingsPicker.model[settingsPicker.currentIndex].image : ""
        }

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width - 32

            anchors {
                left: delegateImage.right
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }

            title: settingsPicker.model.length ? settingsPicker.model[settingsPicker.currentIndex].text : ""
            elide: Text.ElideRight
        }
    }

    background: Rectangle {
        id: backgroundRectangle

        color: ui.ds3.bg.highest
    }
}
