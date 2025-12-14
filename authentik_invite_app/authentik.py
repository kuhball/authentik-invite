from datetime import datetime, timedelta
from typing import List, Optional
import uuid
from authentik_client.exceptions import ApiException
from authentik_client import (
    Configuration,
    ApiClient,
    AdminApi,
    FlowsApi,
    Invitation,
    InvitationRequest,
    StagesApi,
)

from authentik_invite_app.config import settings
from authentik_invite_app.logging import logger


class Authentik:
    def __init__(self):
        configuration = Configuration(
            access_token=settings.authentik_token,
            host=settings.authentik_url,
        )

        with ApiClient(configuration) as api_client:
            self.admin_api_instance = AdminApi(api_client)
            self.stages_api_instance = StagesApi(api_client)
            self.flow_api_instance = FlowsApi(api_client)

        self.enrollment_flow_id = self.get_enrollment_flow_id()

    def get_invitiations(self) -> List[Invitation]:
        try:
            api_response = self.stages_api_instance.stages_invitation_invitations_list()
            return api_response.results
        except ApiException as e:
            logger.error(f"Exception when getting invites: {e}")
            return []

    def get_enrollment_flow_id(self) -> Optional[uuid.UUID]:
        """Fetch all enrollment flows and use the first id."""
        try:
            api_response = self.flow_api_instance.flows_instances_list(
                designation="enrollment"
            )
            return api_response.results[0].pk
        except ApiException as e:
            logger.error(f"Exception while getting flows: {e}")
            return None

    def check_user_invite(self, username: str) -> Optional[Invitation]:
        for invite in self.get_invitiations():
            if username in invite.name:
                return invite
        return None

    def generate_invite(self, username: str) -> Optional[Invitation]:
        try:
            logger.info(f"Generating invite for user {username}.")
            invitation_request = InvitationRequest(
                name=f"user-{username}-invite",
                expires=datetime.now() + timedelta(hours=settings.invite_expire),
                single_use=settings.invite_single_use,
                flow=self.enrollment_flow_id,
            )
            api_response = (
                self.stages_api_instance.stages_invitation_invitations_create(
                    invitation_request
                )
            )
            return api_response
        except Exception as e:
            logger.error(f"Error creating a invite for user {username}: {e}")
            return None


authentik = Authentik()
