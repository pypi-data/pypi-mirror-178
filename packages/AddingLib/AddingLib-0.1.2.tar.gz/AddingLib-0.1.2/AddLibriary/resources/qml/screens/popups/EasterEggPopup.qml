import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "easterEggPopup"
    width: application.width
    height: application.height
    closePolicy: Popup.NoAutoClose

    modal: true
    focus: true

    anchors.centerIn: parent

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.4
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    onOpened: {
        captionsAnim.start()
    }

    PropertyAnimation {
        id: captionsAnim
        target: captionsItem
        to: 0 - captionsItem.height
        duration: 10000
        property: "y"
        onFinished: {
            popup.close()
        }
    }

    contentItem: Item {
        anchors.fill: parent

        Item {
            id: captionsItem
            y: parent.height
            width: 500
            height: 1300
            anchors.horizontalCenter: parent.horizontalCenter

            Custom.FontText {
                id: heroesTitle
                text: "Eternal glory to the heroes:"
                width: parent.width
                height: contentHeight
                color: ui.colors.white
                opacity: 0.9
                font.pixelSize: 32
                font.family: "Open Sans"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                anchors.top: parent.top
            }

            Column {
                id: heroesColumn
                spacing: 80
                width: parent.width
                anchors {
                    top: heroesTitle.bottom
                    topMargin: 128
                    bottom: parent.bottom
                }

                Item {
                    id: managementItem
                    width: parent.width
                    height: managementText.height + managementBody.height + 24

                    Custom.FontText {
                        id: managementText
                        text: "Management"
                        width: parent.width
                        height: contentHeight
                        color: ui.colors.white
                        opacity: 0.9
                        font.pixelSize: 20
                        font.family: "Open Sans"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Column {
                        id: managementBody
                        spacing: 10
                        width: parent.width
                        anchors {
                            top: managementText.bottom
                            topMargin: 24
                        }

                        Repeater {
                            model: ["Alexandr Buksha", "Tetiana Pentsak", "Konstantin Karnaukh"]
                            delegate: Custom.FontText {
                                text: modelData
                                width: parent.width
                                height: contentHeight
                                color: ui.colors.white
                                opacity: 0.9
                                font.pixelSize: 26
                                font.family: "Open Sans"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }

                Item {
                    id: designItem
                    width: parent.width
                    height: designText.height + designBody.height + 24

                    Custom.FontText {
                        id: designText
                        text: "Design Team"
                        width: parent.width
                        height: contentHeight
                        color: ui.colors.white
                        opacity: 0.9
                        font.pixelSize: 20
                        font.family: "Open Sans"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Column {
                        id: designBody
                        spacing: 10
                        width: parent.width
                        anchors {
                            top: designText.bottom
                            topMargin: 24
                        }

                        Repeater {
                            model: ["Sasha Astron", "R.I.P Egor Tatarenko"]
                            delegate: Custom.FontText {
                                text: modelData
                                width: parent.width
                                height: contentHeight
                                color: ui.colors.white
                                opacity: 0.9
                                font.pixelSize: 26
                                font.family: "Open Sans"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }

                Item {
                    id: desktopItem
                    width: parent.width
                    height: desktopText.height + desktopBody.height + 24

                    Custom.FontText {
                        id: desktopText
                        text: "Desktop Team"
                        width: parent.width
                        height: contentHeight
                        color: ui.colors.white
                        opacity: 0.9
                        font.pixelSize: 20
                        font.family: "Open Sans"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Column {
                        id: desktopBody
                        spacing: 10
                        width: parent.width
                        anchors {
                            top: desktopText.bottom
                            topMargin: 24
                        }

                        Repeater {
                            model: ["Mykhailo Kozliuk", "Nick Borovkov", "Anastasiia Pyltsova", "Alexander Sotishvili", "Stepan Rasputnyi"]
                            delegate: Custom.FontText {
                                text: modelData
                                width: parent.width
                                height: contentHeight
                                color: ui.colors.white
                                opacity: 0.9
                                font.pixelSize: 26
                                font.family: "Open Sans"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }

                Item {
                    id: csaItem
                    width: parent.width
                    height: csaText.height + csaBody.height + 24

                    Custom.FontText {
                        id: csaText
                        text: "CSA Team"
                        width: parent.width
                        height: contentHeight
                        color: ui.colors.white
                        opacity: 0.9
                        font.pixelSize: 20
                        font.family: "Open Sans"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Column {
                        id: csaBody
                        spacing: 10
                        width: parent.width
                        anchors {
                            top: csaText.bottom
                            topMargin: 24
                        }

                        Repeater {
                            model: ["Oleksandr Berezianskyi", "Ievgen Kolomiiets", "Yevhenii Semenov", "Mykhailo Ovsiichuk", "Vadim Dihtiar", "Mykhailo Oleksiuk", "Dmitriy Mironiyk"]
                            delegate: Custom.FontText {
                                text: modelData
                                width: parent.width
                                height: contentHeight
                                color: ui.colors.white
                                opacity: 0.9
                                font.pixelSize: 26
                                font.family: "Open Sans"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }
            }
        }
    }
}