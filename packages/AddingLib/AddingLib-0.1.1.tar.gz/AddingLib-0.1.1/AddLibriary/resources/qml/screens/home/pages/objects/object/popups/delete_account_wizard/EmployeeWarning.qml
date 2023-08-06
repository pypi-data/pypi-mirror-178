import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: employeeWarningPopup

    property var companies: []
    property bool isOwner

    width: 500
    height: maxPopupHeight

    modal: true
    focus: true

    header: DS3.NavBarModal {
        onClosed: () => employeeWarningPopup.close()
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        id: infoContainer

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/views_icons/DeleteAccountBlocked.svg"
        titleComponent.text: isOwner ? tr.delete_account_owner_title : tr.delete_account_employee_title
        descComponent.text: isOwner ? tr.delete_account_owner_descr : tr.delete_account_employee_descr
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        id: titleSection

        text: tr.companies
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    Column {
        width: parent.width

        spacing: 1

        Repeater {
            id: companiesRepeater

            width: parent.width

            model: employeeWarningPopup.companies

            DS3.SettingsContainerItem {
                width: parent.width
                height: infoImage.height

                isFirst: index == 0
                isLast: index == companiesRepeater.count - 1

                DS3.InfoImage {
                    id: infoImage

                    width: parent.width

                    atomTitle.title: modelData.company.name
                    companyImage.source: modelData.company && modelData.company.logo && modelData.company.logo.images ?
                        util.get_image_with_resolution(modelData.company.logo.images, "64x64")
                        :
                        ""
                    color: ui.ds3.figure.transparent
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    footer: Item {}
}