import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {
    id: popup

    width: 330

    property string installerName
    property string requestedHours
    property var companyExpirationTimestamp
    property var requestId
    property bool isPermanentCompanyAccess: false
    property bool companyHasEnoughHours: true
    property bool isRequestPermanent: requestedHours == "PERMANENT"
    property var companyPermissionsSecondsLeft: 0

    function calculateCompanyPermissionsSecondsLeft() {
        companyPermissionsSecondsLeft = Math.round(companyExpirationTimestamp - Date.now() / 1000)
    }

    function checkCompanyHasEnoughHours() {
        // minus 60 seconds to prevent timing issues
        return companyPermissionsSecondsLeft - 3600 * requestedHours - 60 > 0
    }

    title: companyHasEnoughHoursContent.visible
        ? tr.installer_requested_access_desktop_title
        : tr.not_enough_rights_company_desktop_title

    onAboutToShow: {
        calculateCompanyPermissionsSecondsLeft()
        if (!isPermanentCompanyAccess) {
            companyHasEnoughHours = checkCompanyHasEnoughHours()
            timer.start()
        }
    }

    Timer {
        id: timer

        interval: 20000
        repeat: true
        triggeredOnStart: true

        onTriggered: {
            if (!checkCompanyHasEnoughHours()) {
                timer.stop()
                companyHasEnoughHours = false
            }
            else {
                calculateCompanyPermissionsSecondsLeft()
            }
        }
    }

    Column {
        id: companyHasEnoughHoursContent

        width: parent.width

        visible: companyHasEnoughHours

        DS3.Text {
            id: descriptionText1

            width: parent.width

            style: ui.ds3.text.body.SRegular
            color: ui.colors.secondary
            horizontalAlignment: Text.AlignHCenter

            Connections {
                target: popup

                onCompanyPermissionsSecondsLeftChanged: {
                    if (isRequestPermanent) descriptionText1.text = util.insert(
                        tr.installer_requested_permanent_access_desktop_descr, [
                            installerName
                        ]
                    )
                    else if (isPermanentCompanyAccess) descriptionText1.text = util.insert(
                        tr.installer_requested_access_desktop, [
                            "", // due to the same key that is used in journal
                            installerName,
                            "", // also
                            requestedHours
                        ]
                    )
                    else descriptionText1.text = util.insert(
                        tr.installer_requested_access_desktop_descr, [
                            installerName,
                            requestedHours,
                            Math.floor(companyPermissionsSecondsLeft / 3600),
                            Math.floor((companyPermissionsSecondsLeft % 3600) / 60)
                        ]
                    )
                }
            }
        }

        DS3.Spacing { height: 32 }

        DS3.ButtonContained {
            width: parent.width

            text: tr.approve

            onClicked: app.facility_module.process_hub_permissions_for_employee_request(true, requestId)
        }

        DS3.Spacing { height: 16 }

        DS3.ButtonOutlined {
            width: parent.width

            text: tr.decline
            isAttention: true

            onClicked: app.facility_module.process_hub_permissions_for_employee_request(false, requestId)
        }
    }

    Column {
        id: companyHasNotEnoughHoursContent

        width: parent.width

        visible: !companyHasEnoughHoursContent.visible

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.SRegular
            text: isRequestPermanent
                ? util.insert(tr.not_enough_permanent_rights_company_desktop_descr1, [installerName])
                : util.insert(tr.not_enough_rights_company_desktop_descr1, [installerName, requestedHours])
            color: ui.colors.secondary
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.Spacing { height: 8 }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.SRegular
            text: tr.not_enough_rights_company_desktop_descr2
            horizontalAlignment: Text.AlignHCenter
            color: ui.colors.secondary
        }

        DS3.Spacing { height: 32 }

        DS3.ButtonContained {
            width: parent.width

            text: tr.request_from_hub_admin

            onClicked: app.facility_module.claim_hub_company_permissions_for_employee(requestId)
        }

        DS3.Spacing { height: 16 }

        DS3.ButtonOutlined {
            width: parent.width

            text: tr.decline
            isAttention: true

            onClicked: app.facility_module.process_hub_permissions_for_employee_request(false, requestId)
        }
    }

    Connections {
        target: app

        onActionSuccess: popup.close()
        onActionFailed: popup.close()
    }
}
