import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts"


Rectangle {
    id: delegate

    width: parent.width
    height: delegateRow.height + 15

    color: ui.ds3.bg.base

    RowLayout {
        id: delegateRow

        width: parent.width

        Layout.fillHeight: true
        spacing: 15

        anchors.centerIn: parent

        Row {
            spacing: 15
            Layout.preferredWidth: 300

            DS3.CompanyImage {
                width: 64
                height: 64

                source: logo || ""
                name: company_name
            }

            Column {
                id: companyInfo

                width: 214

                spacing: 12

                DS3.Text {
                    width: parent.width

                    text: company_name
                    style: ui.ds3.text.body.LRegular
                    color: ui.ds3.figure.base
                }

                DS3.Text {
                    width: parent.width

                    text: locations
                    style: ui.ds3.text.body.SRegular
                    color: ui.ds3.figure.secondary
                }
            }
        }

        ColumnLayout {
            id: companyNumbers

            Layout.preferredWidth: 200
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignTop

            spacing: 12

            Repeater {
                model: phone_numbers

                Stack {
                    titleText: modelData.description
                    sectionText: modelData.number
                }
            }
        }

        Column {
            id: companyAddress

            Layout.preferredWidth: 300

            Stack {
                visible: web_site_url
                titleText: tr.website
                sectionText: web_site_url
            }

            Repeater {
                model: customer_inquiries_emails

                Stack {
                    visible: modelData
                    titleText: tr.a911_mail
                    sectionText: modelData.email
                }
            }
        }

        Row {
            width: 200
            Layout.preferredWidth: 150

            spacing: 8

            Image {
                sourceSize.width: 24
                sourceSize.height: 24

                source: {
                    return {
                        PENDING_APPROVAL: "qrc:/resources/images/icons/binding-pending-approval.svg",
                        APPROVED: "qrc:/resources/images/icons/binding-active.svg",
                        IN_SLEEP_MODE: "qrc:/resources/images/icons/binding-sleep.svg",
                    }[monitoring_status] || "qrc:/resources/images/icons/binding-no-object.svg"
                }
            }

            DS3.Text {
                width: parent.width

                style: ui.ds3.text.body.LRegular
                text: {
                    return {
                        PENDING_APPROVAL: tr.binding_status_pending_approval,
                        APPROVED: tr.active,
                        IN_SLEEP_MODE: tr.a911_sleeping,
                    }[monitoring_status] || tr.no_object_911
                }
            }
        }
    }

    Divider {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
    }
}