import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
//  Choose one of three properties below
    enum ImageType {
        None,
        PlugImage,    // 88x88
        DeviceImage,  // 96x96
        DeviceLargeImage, // 128x128
        BigImage,     // 136x136
        WizardImage  // 375x166
    }
    property var imageType: DS3.InfoContainer.ImageType.None

//  Main image source (plugImage: 88x88, deviceImage: 96x96, HubHybrid image: 136x136)
    property string imageSource: ""
//  Image visibility
    readonly property bool hasImage: imageType != InfoContainer.ImageType.None
//  Spinner visibility
    property bool hasSpinner: false

//  Title text
    property alias titleComponent: titleComponent
//  Description text
    property alias descComponent: descComponent

    width: parent.width
    height: content.height

    Column {
        id: content

        width: parent.width - 32

        anchors.horizontalCenter: parent.horizontalCenter

        Item {
            id: image

            width: parent.width
            height: hasImage? 136 : 0

            DS3.PlugImage { // Component for plug image
                id: plugImage

                anchors.horizontalCenter: parent.horizontalCenter

                visible: imageType == InfoContainer.ImageType.PlugImage
                source: imageSource
            }

            DS3.Image {  // Component for device image or HubHybrid image
                id: deviceImage

                anchors.centerIn: parent

                width: {
                    if (imageType == InfoContainer.ImageType.DeviceImage) return 96
                    if (imageType == InfoContainer.ImageType.WizardImage) return 375
                    if (imageType == InfoContainer.ImageType.DeviceLargeImage) return 128
                    return 136
                }
                height: {
                    if (imageType == InfoContainer.ImageType.DeviceImage) return 96
                    if (imageType == InfoContainer.ImageType.WizardImage) return 166
                    if (imageType == InfoContainer.ImageType.DeviceLargeImage) return 128
                    return 136
                }

                visible: imageType != InfoContainer.ImageType.PlugImage
                source: imageSource
            }

            DS3.Spinner {
                anchors.centerIn: parent

                visible: hasSpinner
            }
        }

        DS3.Spacing {
            height: 24

            visible: hasImage
        }

        DS3.TitleUniversal {
            id: titleComponent

            width: parent.width

            visible: !!text
        }

        DS3.Spacing {
            height: 8

            visible: titleComponent.visible && descComponent.visible
        }

        DS3.Text {
            id: descComponent

            width: parent.width

            horizontalAlignment: Text.AlignHCenter
            style: ui.ds3.text.body.LRegular
            color: ui.ds3.figure.secondary
            visible: !!text
        }
    }
}
