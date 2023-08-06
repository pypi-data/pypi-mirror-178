import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
    id: gifIcon
    width: 20
    height: 20
    anchors.centerIn: parent

    property var count: 0
    property var running: false
    property var interval: 500
    property var currentIndex: 0

    Loader {
        id: animLoader
        anchors.fill: parent
        sourceComponent: {
            if (gifIcon.count == 1) return points1
            if (gifIcon.count == 2) return points2
            if (gifIcon.count == 3) return points3
            if (gifIcon.count == 4) return points4
            if (gifIcon.count == 5) return points5
            return undefined
        }
    }

    Component {
        id: points1

        Item {
            width: 16
            height: 16

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: ui.colors.green1
                anchors.centerIn: parent
            }
        }
    }

    Component {
        id: points2

        Item {
            width: 16
            height: 16

            property var currentIndex: gifIcon.currentIndex

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    left: parent.left
                    leftMargin: 2
                    verticalCenter: parent.verticalCenter
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    right: parent.right
                    rightMargin: 2
                    verticalCenter: parent.verticalCenter
                }
            }
        }
    }

    Component {
        id: points3

        Item {
            width: 16
            height: 16

            property var currentIndex: gifIcon.currentIndex

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    verticalCenter: parent.verticalCenter
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 2 ? ui.colors.green1 : ui.colors.white
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                }
            }

            /*Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 1
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    right: parent.right
                    bottom: parent.bottom
                    bottomMargin: 1
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 2 ? ui.colors.green1 : ui.colors.white
                anchors {
                    left: parent.left
                    bottom: parent.bottom
                    bottomMargin: 1
                }
            }*/
        }
    }

    Component {
        id: points4

        Item {
            width: 16
            height: 16

            property var currentIndex: gifIcon.currentIndex

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 4
                    left: parent.left
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 4
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 2 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 4
                    right: parent.right
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 3 ? ui.colors.green1 : ui.colors.white
                anchors {
                    verticalCenter: parent.verticalCenter
                    verticalCenterOffset: 4
                    left: parent.left
                }
            }

            /*Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 2 ? ui.colors.green1 : ui.colors.white
                anchors {
                    bottom: parent.bottom
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 3 ? ui.colors.green1 : ui.colors.white
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }
            }*/
        }
    }

    Component {
        id: points5

        Item {
            width: 16
            height: 16

            property var currentIndex: gifIcon.currentIndex

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 4
                    left: parent.left
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 4
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 2 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    topMargin: 4
                    right: parent.right
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 3 ? ui.colors.green1 : ui.colors.white
                anchors {
                    verticalCenter: parent.verticalCenter
                    verticalCenterOffset: 4
                    left: parent.left
                }
            }

            Rectangle {
                width: 4
                height: width
                radius: height / 2
                color: parent.currentIndex == 4 ? ui.colors.green1 : ui.colors.white
                anchors {
                    verticalCenter: parent.verticalCenter
                    verticalCenterOffset: 4
                    horizontalCenter: parent.horizontalCenter
                }
            }

            /*Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 0 ? ui.colors.green1 : ui.colors.white
                anchors {
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 1 ? ui.colors.green1 : ui.colors.white
                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                    verticalCenterOffset: -1
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 2 ? ui.colors.green1 : ui.colors.white
                anchors {
                    right: parent.right
                    rightMargin: 2
                    bottom: parent.bottom
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 3 ? ui.colors.green1 : ui.colors.white
                anchors {
                    left: parent.left
                    leftMargin: 2
                    bottom: parent.bottom
                }
            }

            Rectangle {
                width: 6
                height: width
                radius: height / 2
                color: parent.currentIndex == 4 ? ui.colors.green1 : ui.colors.white
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                    verticalCenterOffset: -1
                }
            }*/
        }
    }
}