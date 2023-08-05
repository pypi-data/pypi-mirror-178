"""Invoices API endpoint"""
from datetime import datetime
from typing import Union

from .enums import CancellationReason
from .http import BaseClient


class InvoicesClient(BaseClient):
    """Products API client"""

    endpoint = "invoices"

    def create(self, data: dict) -> dict:
        """Creates a new invoice

        Args:
            data (dict): Invoice data

        Returns:
            dict: Created invoice object
        """
        url = self._get_request_url()
        return self._execute_request("POST", url, json_data=data).json()

    def all(
        self,
        search: str = None,
        customer_id: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        page: int = None,
        limit: int = None,
    ) -> dict:
        """Returns a paginated list of all invoices in an organization
        or makes a search according to parameters

        Args:
            search (str, optional): Text to search on the invoice. Defaults to None.
            customer_id (str, optional): Id of the customer. Useful to get invoices issued to a
            single customer. Defaults to None.
            start_date (datetime, optional): Lower limit of a date range. Defaults to None.
            end_date (datetime, optional): Upper limit of a date range. Defaults to None.
            page (int, optional): Result page to return, beginning with 1. Defaults to None.
            limit (int, optional): Number from 1 to 50 representing the maximum quantity of
            results to return. Used for pagination. Defaults to None.

        Returns:
            dict: List of invoices
        """
        params = {}
        if search:
            params.update({"q": search})

        if customer_id:
            params.update({"customer": customer_id})

        if start_date:
            params.update({"date[gt]": start_date.astimezone().isoformat()})

        if end_date:
            params.update({"date[lt]": end_date.astimezone().isoformat()})

        if page:
            params.update({"page": page})

        if limit:
            params.update({"limit": limit})

        url = self._get_request_url()
        return self._execute_request("GET", url, params).json()

    def retrieve(self, invoice_id: str) -> dict:
        """Retrieves a single invoice object

        Args:
            invoice_id (str): ID of the invoice to retrieve

        Returns:
            dict: Invoice object
        """
        url = self._get_request_url([invoice_id])
        return self._execute_request("GET", url).json()

    def cancel(
        self,
        invoice_id: str,
        reason: Union[CancellationReason, str],
        substitution: str = None,
    ) -> dict:
        """Cancels an invoice. The invoice will not be valid anymore and will
        change its status to canceled

        Args:
            invoice_id (str): Invoice ID to cancel
            reason (CancellationReason): Reason for cancellation
            substitution (str, optional): Substitute invoice id. Defaults to None.

        Returns:
            dict: Cancelled invoice object
        """
        params = {}
        if reason:

            motive = reason.value if isinstance(reason, CancellationReason) else reason
            params.update({"motive": motive})

        if substitution:
            params.update({"substitution": substitution})

        url = self._get_request_url([invoice_id])
        return self._execute_request("DELETE", url, query_params=params).json()

    def get_cancellation_receipt(self, invoice_id: str) -> str:
        """Get XML cancellation receipt of an invoice as str

        Args:
            invoice_id (str): Id of cancelled invoice

        Returns:
            str: XML cancellation receipt
        """
        url = self._get_request_url([invoice_id, "cancellation_receipt", "xml"])
        return self._execute_request("GET", url).text

    def download_pdf(self, invoice_id: str) -> bytes:
        """Download invoice PDF file

        Args:
            invoice_id (str): Id of invoice

        Returns:
            bytes: Invoice PDF file
        """
        url = self._get_download_file_url("pdf", invoice_id)
        return self._execute_request("GET", url).content

    def download_xml(self, invoice_id: str) -> bytes:
        """Download invoice XML file

        Args:
            invoice_id (str): Id of invoice

        Returns:
            bytes: Invoice XML file
        """
        url = self._get_download_file_url("xml", invoice_id)
        return self._execute_request("GET", url).content

    def download_zip(self, invoice_id: str) -> bytes:
        """Download invoice ZIP file

        Args:
            invoice_id (str): Id of invoice

        Returns:
            bytes: Invoice ZIP file
        """
        url = self._get_download_file_url("zip", invoice_id)
        return self._execute_request("GET", url).content

    def send_by_email(self, invoice_id: str, email: str = None) -> dict:
        """Send an email to your client's address, with the XML and PDF files attached to the
        message

        Args:
            invoice_id (str): Id of invoice
            email (str, optional): Email address to send the invoice. If this parameter is None,
            the invoice will be sent to the email that the customer has registered.
            Defaults to None.

        Returns:
            dict: Response message
        """
        url = self._get_request_url([invoice_id, "email"])
        data = {"email": email} if email else {}
        return self._execute_request("POST", url, json_data=data).json()
