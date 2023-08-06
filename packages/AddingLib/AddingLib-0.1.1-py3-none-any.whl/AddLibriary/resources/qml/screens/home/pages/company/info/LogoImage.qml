import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: logoImage

    property alias source: logoImageSource.source
    property string imageId
    property bool editMode: false

    function error() {
        placeholder.border.width = 1
    }

    function deleteImage() {
        logoImageSource.source = ""
        imageId = ""
    }

    width: 200
    height: 200

    Rectangle {
        id: placeholder

        anchors.fill: logoImageSource

        visible: !!logoImageSource

        radius: 8
        color: ui.backgrounds.lowest

        border.width: 0
        border.color: ui.colors.attention

        DS3.Text {
            anchors.centerIn: parent
            style:  {
                "size": 64,
                "height": 64,
                "weight": 75
            }
            text: companyName[0].toUpperCase()
            color: ui.ds3.figure.nonessential
            horizontalAlignment: Text.AlignHCenter
            visible: !loadingAnimation.running
        }

        Item {
            id: loadingItem

            width: 50
            height: 50

            anchors.centerIn: parent

            RotationAnimator on rotation {
                id: loadingAnimation

                from: 0
                to: 360
                loops: Animation.Infinite
                running: false
                duration: 1000
                easing.type: Easing.InOutQuad
            }

            Rectangle {
                width: 7
                height: 7

                anchors {
                    top: parent.top
                    horizontalCenter: parent.horizontalCenter
                }

                color: ui.backgrounds.highest
                radius: 7
                visible: loadingAnimation.running
            }
        }
    }

    Image {
        id: logoImageSource

        width: 200
        height: 200

        visible: !loadingAnimation.running
        fillMode: Image.PreserveAspectCrop
        layer.enabled: true
        layer.effect: OpacityMask {
            maskSource: logoMask
        }

        onStatusChanged: {
            if (status == Image.Loading) {
                loadingAnimation.running = true
            } else {
                loadingAnimation.running = false
            }
        }
    }

    DS.ButtonRound {
        anchors {
            top: parent.top
            right: parent.right
            margins: 12
        }

        visible: !!logoImage.imageId && !loadingAnimation.running && editMode
        style: ui.controls.minus

        onClicked: {
            logoImage.deleteImage()
        }
    }

    Rectangle {
        id: logoMask

        anchors.fill: logoImageSource
        visible: false
        radius: 8
    }

    Connections {
        target: app.company_module

        onUploadCompanyLogoSuccess: {
            if (editMode) {
                logoImage.source = logo_url
                logoImage.imageId = image_id
                placeholder.border.width = 0
            }
        }

        onToggleCompanyLogoAnimation: {
            if (editMode) {
                if (on) loadingAnimation.running = true
                else loadingAnimation.running = false
            }
        }
    }
}
