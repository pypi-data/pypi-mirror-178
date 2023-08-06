import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts"
import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
    id: delegate
    property alias flow: flow

    opacity: hub.online ? 1: 0.3

    Image {
        id: deviceImage

        width: 64
        height: 64

        anchors {
            left: parent.left
            leftMargin: 8
            top: parent.top
            topMargin: 4
        }

        source: Images.get_image(hub.image_type_name, "Medium", hub.color)

        /* ------------------------------------------------ */
        /* desktop tests */
        Accessible.name: {
            if (!delegate.parent.parent.accessiblePrefix) return ""
            return __accessible_unique_ids__ ? delegate.parent.parent.accessiblePrefix + "_image" : "image"
        }
        Accessible.description: source
        Accessible.role: Accessible.Graphic
        /* ------------------------------------------------ */
    }

    DS3.Text {
        id: deviceName

        width: delegate.width - (deviceDelegate.settingsVisible ? 144 : 96)

        anchors {
            top: parent.top
            topMargin: 8
            left: deviceImage.right
            leftMargin: 12
        }

        color: ui.colors.light1
        text: device.name

            /* ------------------------------------------------ */
            /* desktop tests */
            Accessible.name: {
                if (!delegate.parent.parent.accessiblePrefix) return ""
                return __accessible_unique_ids__ ? delegate.parent.parent.accessiblePrefix + "_name" : "name"
            }
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ------------------------------------------------ */
    }

    DS3.BadgeAttention {
        id: issues

        anchors {
            left: delegate.left
            top: delegate.top
        }

        visible: device.issue_count > 0
        text: device.issue_count
    }

    Flow {
        id: flow

        width: 160
        height: childrenRect.height

        anchors {
            left: deviceImage.right
            leftMargin: 12
            bottom: parent.bottom
            bottomMargin: 8
        }

        spacing: 8
        opacity: (!!hub && hub.online) ? 1 : 0.4

        FlowIco{}
    }

    Item {
        id: updateButtonWrapper

        width: 40
        height: 22

        anchors {
            top: parent.top
            topMargin: 24
            right: parent.right
            rightMargin: deviceDelegate.settingsVisible ? 60 : 16
        }

        enabled: device.online
        opacity: enabled ? 1 : 0.5

        Rectangle {
            id: updateButton

            width: 40
            height: 22

            radius: height/2
            color: "#f64347"
            visible: {
                if (hub.firmware_version_dec < 207000) {
                    if (!(!hub.hub_autoupdate && hub.firmware_available)) return false
                    if (hub.current_user.fw_updates_access) {
                        return true
                    }
                    return false
                } else {
                    if (!(!hub.hub_autoupdate && (hub.firmware_available || hub.is_rex_update_needed))) {
                        return false
                    }
                    if (hub.current_user.fw_updates_access) {
                        return true
                    }
                    return false
                }
            }

            Image {
                id: downloadImg

                width: 16
                height: 16

                anchors.centerIn: parent

                visible: false
                source: "qrc:/resources/images/desktop/icons/ic-hub-update.png"
            }

            ColorOverlay {
                anchors.fill: downloadImg

                source: downloadImg
                color: ui.colors.light1
            }

            MouseArea {
                anchors.fill: parent

                enabled: hub.online
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    function todo() {
                        app.hub_management_module.start_firmware_update()
                    }
                    DesktopPopups.confirm_or_cancel(tr.warning, tr.software_updates_available + ' ' + hub.latest_available_version, todo, tr.update_firmware)
                }
            }
        }
    }

    Item {
        id: billing

        property var model: management.companies.billing

        width: parent.width - 32
        height: column.height

        anchors {
            top: flow.bottom
            topMargin: 16
            horizontalCenter: parent.horizontalCenter
        }

        Column {
            id: column

            width: parent.width
            spacing: 1

            Repeater {
                width: parent.width
                model: billing.model

                delegate: Custom.RoundedRect {
                    width: parent.width
                    height: 66

                    clip: true
                    color: ui.colors.dark3
                    radius: 8

                    topLeftCorner: index == 0
                    topRightCorner: index == 0
                    bottomRightCorner: index == billing.model.length - 1
                    bottomLeftCorner: index == billing.model.length - 1

                    Item {
                        id: companyImageItem

                        width: 42
                        height: 42

                        anchors {
                            left: parent.left
                            leftMargin: 16
                            verticalCenter: parent.verticalCenter
                        }

                        Image {
                            id: additionalImage

                            source: ""
                            mipmap: true
                            visible: false

                            onStatusChanged: {
                                if (status == Image.Error || status == Image.Null || status == Image.Loading) {
                                    companyImage.source = "qrc:/resources/images/desktop/defaults/default_company_logo.png"
                                } else {
                                    companyImage.source = source
                                }
                            }
                        }

                        Image {
                            id: companyImage

                            width: companyImageItem.width
                            height: companyImageItem.height

                            anchors.fill: parent

                            mipmap: true
                            visible: false
                            source: "qrc:/resources/images/desktop/defaults/default_company_logo.png"
                        }

                        OpacityMask {
                            anchors.fill: companyImage
                            source: companyImage

                            maskSource: Rectangle {
                                width: companyImageItem.width
                                height: companyImageItem.height
                                radius: 4
                                visible: false
                            }
                        }
                    }

                    Custom.FontText {
                        id: companyName

                        width: parent.width - 200
                        height: parent.height

                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: companyImageItem.right
                            leftMargin: 16
                        }

                        color: ui.colors.light2
                        text: modelData.company_name

                        wrapMode: Text.Wrap
                        maximumLineCount: 3
                        elide: Text.ElideRight
                        textFormat: Text.PlainText
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }

                    Custom.FontText {
                        id: balance

                        anchors {
                            top: parent.top
                            topMargin: 12
                            right: parent.right
                            rightMargin: 16
                        }

                        color: modelData.balance > 0 ? ui.colors.lime1: ui.colors.red1
                        text: modelData.balance + " " + modelData.currency
                        font.pixelSize: 16
                        textFormat: Text.AutoText
                    }

                    Custom.FontText {
                        id: nextPaymentDay

                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 12
                            right: parent.right
                            rightMargin: 16
                        }

                        color: modelData.balance > 0 ? ui.colors.middle1: ui.colors.red1
                        text: {
                            if (modelData.balance > 0) {
                                var npd = Date.fromLocaleString(application.locale, modelData.next_payment_date, "yyyy-MM-dd")
                                return util.insert(tr.till_date, [npd.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.ShortFormat))])
                            }
                            return tr.fill_account
                        }
                        font.pixelSize: 12
                        textFormat: Text.AutoText
                    }

                    Connections {
                        target: app

                        onGetCompanyInfoForBilling: {
                            if (modelData.company_id == response.company_id) {
                                companyName.text = response.name
                                additionalImage.source = response.logo
                            }
                        }
                    }

                    Component.onCompleted: {
                        app.get_company_info_for_billing(hub.hub_id, modelData.company_id)
                    }
                }
            }
        }

        ToolTip {
            id: toolTip

            width: 260
            height: contentText.contentHeight + 24

            x: parent.width + 42
            y: (billing.height - toolTip.height) / 2

            visible: billingTipArea.containsMouse

            contentItem: Custom.FontText {
                id: contentText

                anchors.centerIn: parent

                color: ui.colors.light3
                text: tr.billing_warning_info
                font.pixelSize: 12
                wrapMode: Text.Wrap
                textFormat: Text.PlainText
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                anchors.fill: parent

                radius: 8
                color: ui.colors.dark4
            }
        }

        Custom.HandMouseArea {
            id: billingTipArea

            propagateComposedEvents: true
        }
    }
}
