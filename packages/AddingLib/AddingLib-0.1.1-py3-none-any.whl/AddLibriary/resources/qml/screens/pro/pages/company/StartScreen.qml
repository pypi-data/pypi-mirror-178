import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: companyStartScreen

    Item {
        id: startScreenHeader

        width: parent.width * 0.6
        height: 80

        anchors {
            top: parent.top
            topMargin: 32
            horizontalCenter: parent.horizontalCenter
        }

        Custom.FontText {
            id: startScreenHeaderText

            text: tr.create_company_title
            color: ui.colors.light3

            font.pixelSize: 32
            font.bold: true
            maximumLineCount: 2
            wrapMode: Text.Wrap
            elide: Text.ElideRight
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent
        }
    }

    Item {
        id: startScreenExplain

        width: parent.width * 0.4
        height: 48

        anchors {
            top: startScreenHeader.bottom
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }

        Custom.FontText {
            id: startScreenExplainText

            text: tr.create_company_why
            color: ui.colors.light3

            font.pixelSize: 16
            maximumLineCount: 2
            wrapMode: Text.Wrap
            elide: Text.ElideRight
            textFormat: Text.PlainText
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter

            anchors.fill: parent
        }
    }


    Item {
        id: startScreenGrid

        width: parent.width - 240

        property var gridWidth: width / 3 - 16
        property var gridHeight: height / 2 - 8

        anchors {
            top: startScreenExplain.bottom
            topMargin: 32
            bottom: startScreenCreate.top
            bottomMargin: 32
            horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            clip: true
            width: parent.gridWidth
            height: parent.gridHeight
            radius: 10
            color: ui.colors.dark4

            anchors {
                top: parent.top
                left: parent.left
            }

            Image {
                source: "qrc:/resources/images/pro/company/create-company-info-1.svg"
                sourceSize.height: parent.height - 52
                anchors {
                    top: parent.top
                    topMargin: 16
                    right: parent.right
                }
            }

            Item {
                width: parent.width * 0.8
                height: parent.height / 2 - 16

                anchors {
                    left: parent.left
                    leftMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                Custom.FontText {
                    text: tr.create_company_info1
                    color: ui.colors.light3

                    font.pixelSize: 20
                    font.bold: true
                    maximumLineCount: 3
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    verticalAlignment: Text.AlignBottom

                    anchors.fill: parent
                }
            }
        }

        Rectangle {
            clip: true
            width: parent.gridWidth
            height: parent.gridHeight
            radius: 10
            color: ui.colors.dark4

            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
            }

            Image {
                source: "qrc:/resources/images/pro/company/create-company-info-2.svg"
                sourceSize.height: parent.height - 36
                anchors {
                    top: parent.top
                    topMargin: 12
                    right: parent.right
                    rightMargin: 20
                }
            }

            Item {
                width: parent.width * 0.8
                height: parent.height / 2 - 16

                anchors {
                    left: parent.left
                    leftMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                Custom.FontText {
                    text: tr.create_company_info2
                    color: ui.colors.light3

                    font.pixelSize: 20
                    font.bold: true
                    maximumLineCount: 3
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    verticalAlignment: Text.AlignBottom

                    anchors.fill: parent
                }
            }
        }

        Rectangle {
            clip: true
            width: parent.gridWidth
            height: parent.gridHeight
            radius: 10
            color: ui.colors.dark4

            anchors {
                top: parent.top
                right: parent.right
            }

            Image {
                source: "qrc:/resources/images/pro/company/create-company-info-3.svg"
                sourceSize.height: parent.height
                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                }
            }

            Item {
                width: parent.width * 0.8
                height: parent.height / 2 - 16

                anchors {
                    left: parent.left
                    leftMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                Custom.FontText {
                    text: tr.create_company_info3
                    color: ui.colors.light3

                    font.pixelSize: 20
                    font.bold: true
                    maximumLineCount: 3
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    verticalAlignment: Text.AlignBottom

                    anchors.fill: parent
                }
            }
        }

        Rectangle {
            clip: true
            width: parent.gridWidth
            height: parent.gridHeight
            radius: 10
            color: ui.colors.dark4

            anchors {
                left: parent.left
                bottom: parent.bottom
            }

            Image {
                source: "qrc:/resources/images/pro/company/create-company-info-4.svg"
                sourceSize.height: parent.height - 16
                anchors {
                    top: parent.top
                    right: parent.right
                }
            }

            Item {
                width: parent.width * 0.8
                height: parent.height / 2 - 16

                anchors {
                    left: parent.left
                    leftMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                Custom.FontText {
                    text: tr.create_company_info4
                    color: ui.colors.light3

                    font.pixelSize: 20
                    font.bold: true
                    maximumLineCount: 3
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    verticalAlignment: Text.AlignBottom

                    anchors.fill: parent
                }
            }
        }

        Rectangle {
            clip: true
            width: parent.gridWidth
            height: parent.gridHeight
            radius: 10
            color: ui.colors.dark4

            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
            }

            Image {
                source: "qrc:/resources/images/pro/company/create-company-info-5.svg"
                sourceSize.height: parent.height - 48
                anchors {
                    top: parent.top
                    topMargin: 12
                    right: parent.right
                }
            }

            Item {
                width: parent.width * 0.8
                height: parent.height / 2 - 16

                anchors {
                    left: parent.left
                    leftMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                Custom.FontText {
                    text: tr.create_company_info5
                    color: ui.colors.light3

                    font.pixelSize: 20
                    font.bold: true
                    maximumLineCount: 3
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    verticalAlignment: Text.AlignBottom

                    anchors.fill: parent
                }
            }
        }

        Rectangle {
            clip: true
            width: parent.gridWidth
            height: parent.gridHeight
            radius: 10
            color: ui.colors.dark4

            anchors {
                right: parent.right
                bottom: parent.bottom
            }

            Image {
                source: "qrc:/resources/images/pro/company/create-company-info-6.svg"
                sourceSize.height: parent.height - 60
                anchors {
                    top: parent.top
                    topMargin: 16
                    right: parent.right
                    rightMargin: 16
                }
            }

            Item {
                width: parent.width * 0.8
                height: parent.height / 2 - 16

                anchors {
                    left: parent.left
                    leftMargin: 16
                    bottom: parent.bottom
                    bottomMargin: 16
                }

                Custom.FontText {
                    text: tr.create_company_info6
                    color: ui.colors.light3

                    font.pixelSize: 20
                    font.bold: true
                    maximumLineCount: 3
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    verticalAlignment: Text.AlignBottom

                    anchors.fill: parent
                }
            }
        }
    }


    Item {
        id: startScreenCreate

        width: startScreenCreateButton.textButton.contentWidth + 64
        height: 48

        anchors {
            bottom: parent.bottom
            bottomMargin: 32
            horizontalCenter: parent.horizontalCenter
        }

        Custom.Button {
            id: startScreenCreateButton

            width: parent.width
            enabledCustom: true
            text: tr.button_create_company_free
            textButton.textFormat: Text.PlainText

            anchors.centerIn: parent

            onClicked: {
                companyLoader.source = companyStack.searchScreen
            }
        }
    }
}
