from odoo import models, fields, api
from num2words import num2words
from odoo.exceptions import UserError
from odoo.exceptions import UserError
import base64
from datetime import date




class HrForm16(models.Model):
    _name = 'hr.form16'
    _description = 'Form 16'
    # Form 16 Basic Information
    
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)

    certificate_number = fields.Char(string="Certificate Number")
    assessment_year = fields.Char(string="Assessment Year", default="2025-2026")
    period_from = fields.Date(string="Period From", default=fields.Date.today().replace(month=4, day=1))
    period_to = fields.Date(string="Period To", default=fields.Date.today().replace(month=3, day=31))
    pan_number = fields.Char(string="PAN Number")
    
    # Company PAN/TAN
    # company_pan_number = fields.Char(related='company_id.pan_number', string="Company PAN")
    # company_tan_number = fields.Char(related='company_id.tan_number', string="Company TAN")
    
    # Quarterly Data


    q1_amount_paid = fields.Float(string="Q1 Amount Paid", compute="_compute_quarterly_gross")
    q2_amount_paid = fields.Float(string="Q2 Amount Paid", compute="_compute_quarterly_gross")
    q3_amount_paid = fields.Float(string="Q3 Amount Paid", compute="_compute_quarterly_gross")
    q4_amount_paid = fields.Float(string="Q4 Amount Paid", compute="_compute_quarterly_gross")



    # part B - salary details


    salary_sec_17_1 = fields.Float(string="Salary as per sec 17(1)", compute="_compute_quarterly_gross")







    q1_receipt_number = fields.Char(string="Q1 Receipt Number")
    # q1_amount_paid = fields.Float(string="Q1 Amount Paid")  
  
 
    q1_tax_deducted = fields.Float(string="Q1 Tax Deducted")
    q1_tax_deposited = fields.Float(string="Q1 Tax Deposited")
    
    q2_receipt_number = fields.Char(string="Q2 Receipt Number")
    # q2_amount_paid = fields.Float(string="Q2 Amount Paid")

    q2_tax_deducted = fields.Float(string="Q2 Tax Deducted")
    q2_tax_deposited = fields.Float(string="Q2 Tax Deposited")
    
    q3_receipt_number = fields.Char(string="Q3 Receipt Number")
        # q3_amount_paid = fields.Float(string="Q3 Amount Paid")

    q3_tax_deducted = fields.Float(string="Q3 Tax Deducted")
    q3_tax_deposited = fields.Float(string="Q3 Tax Deposited")
    
    q4_receipt_number = fields.Char(string="Q4 Receipt Number")
    # q4_amount_paid = fields.Float(string="Q4 Amount Paid")
    # q4_amount_paid = fields.Float(string="Q4 Amount Paid", compute="_compute_quarterly_gross", store=True)
    q4_tax_deducted = fields.Float(string="Q4 Tax Deducted")
    q4_tax_deposited = fields.Float(string="Q4 Tax Deposited")
    
    # Computed Total Fields
    total_amount_paid = fields.Float(string="Total Amount Paid", compute="_compute_quarterly_gross")
    total_tax_deducted = fields.Float(string="Total Tax Deducted", compute="_compute_totals", store=True)
    total_tax_deposited = fields.Float(string="Total Tax Deposited", compute="_compute_totals", store=True)
    total_tax_deducted_words = fields.Char(string="Total Tax Deducted in Words", compute="_compute_tax_words")
    
    # Part B - Salary Details
    perquisites_sec_17_2 = fields.Float(string="Perquisites u/s 17(2)")
    profits_sec_17_3 = fields.Float(string="Profits in lieu of salary u/s 17(3)")
    gross_salary_total = fields.Float(string="Gross Salary Total", compute="_compute_salary_details", store=True)
    other_employer_salary = fields.Float(string="Salary from Other Employers")
    exempt_allowances = fields.Float(string="Exempt Allowances u/s 10")
    balance_after_exemptions = fields.Float(string="Balance After Exemptions", compute="_compute_salary_details", store=True)
    
    # Deductions
    standard_deduction = fields.Float(string="Standard Deduction u/s 16(1)", default=50000)
    total_deductions = fields.Float(string="Total Deductions", compute="_compute_salary_details", store=True)
    income_chargeable_salary = fields.Float(string="Income Chargeable under Salaries", compute="_compute_salary_details", store=True)
    other_income = fields.Float(string="Other Income")
    total_income_before_deductions = fields.Float(string="Total Income", compute="_compute_salary_details", store=True)
    gross_total_income = fields.Float(string="Gross Total Income", compute="_compute_salary_details", store=True)
    
    # Chapter VI-A Deductions
    epf_employee = fields.Float(string="Employee PF")
    sec_80c_total = fields.Float(string="Section 80C Total", compute="_compute_via_deductions", store=True)
    sec_80ccc = fields.Float(string="Section 80CCC")
    sec_80ccd = fields.Float(string="Section 80CCD")
    sec_80ccd_1b = fields.Float(string="Section 80CCD(1B)")
    sec_80ccd_2 = fields.Float(string="Section 80CCD(2)")
    sec_80ccg = fields.Float(string="Section 80CCG")
    sec_80d = fields.Float(string="Section 80D")
    sec_80e = fields.Float(string="Section 80E")
    sec_80g = fields.Float(string="Section 80G")
    sec_80tta = fields.Float(string="Section 80TTA")
    other_sec_deductions = fields.Float(string="Other Section Deductions")
    
    total_chapter_via_deductions = fields.Float(string="Total Chapter VI-A Deductions", compute="_compute_via_deductions", store=True)
    total_taxable_income = fields.Float(string="Total Taxable Income", compute="_compute_tax_calculations", store=True)
    
    # Tax Calculations
    tax_on_total_income = fields.Float(string="Tax on Total Income", compute="_compute_tax_calculations", store=True)
    credit_87a = fields.Float(string="Credit u/s 87A")
    surcharge = fields.Float(string="Surcharge")
    health_education_cess = fields.Float(string="Health and Education Cess", compute="_compute_tax_calculations", store=True)
    tax_payable = fields.Float(string="Tax Payable", compute="_compute_tax_calculations", store=True)
    relief_sec_89 = fields.Float(string="Relief u/s 89")
    final_tax_payable = fields.Float(string="Final Tax Payable", compute="_compute_tax_calculations", store=True)
    
    # Authorized Signatory
    authorized_signatory_name = fields.Char(string="Authorized Signatory Name")
    authorized_signatory_father_name = fields.Char(string="Signatory Father Name")
    authorized_signatory_designation = fields.Char(string="Signatory Designation")

    # @api.depends('q1_amount_paid', 'q2_amount_paid', 'q3_amount_paid', 'q4_amount_paid',
    #              'q1_tax_deducted', 'q2_tax_deducted', 'q3_tax_deducted', 'q4_tax_deducted',
    #              'q1_tax_deposited', 'q2_tax_deposited', 'q3_tax_deposited', 'q4_tax_deposited')
    # def _compute_totals(self):
    #     for record in self:
    #         record.total_amount_paid = (record.q1_amount_paid + record.q2_amount_paid + 
    #                                    record.q3_amount_paid + record.q4_amount_paid)
    #         record.total_tax_deducted = (record.q1_tax_deducted + record.q2_tax_deducted + 
    #                                     record.q3_tax_deducted + record.q4_tax_deducted)
    #         record.total_tax_deposited = (record.q1_tax_deposited + record.q2_tax_deposited + 
    #                                      record.q3_tax_deposited + record.q4_tax_deposited)


    @api.depends('employee_id', 'assessment_year')
    def _compute_quarterly_gross(self):
        for record in self:
            # Reset
            record.q1_amount_paid = 0.0
            record.q2_amount_paid = 0.0
            record.q3_amount_paid = 0.0
            record.q4_amount_paid = 0.0

            if not record.employee_id or not record.assessment_year:
                continue

            # Parse assessment year e.g. "2025-2026" → start=2025, end=2026
            try:
                start_year, end_year = record.assessment_year.split('-')
                start_year = int(start_year)
                end_year = int(end_year)
            except Exception:
                continue

            # Financial Year: Apr 1 start_year → Mar 31 end_year
            fy_start = date(start_year, 4, 1)
            fy_end   = date(end_year, 3, 31)

            # Quarter month ranges (financial year based)
            quarters = {
                'q1': [4, 5, 6],        # Apr, May, Jun
                'q2': [7, 8, 9],        # Jul, Aug, Sep
                'q3': [10, 11, 12],     # Oct, Nov, Dec
                'q4': [1, 2, 3],        # Jan, Feb, Mar
            }

            # Fetch all confirmed payslips for this employee in the FY
            payslips = self.env['hr.payslip'].search([
                ('employee_id', '=', record.employee_id.id),
                ('date_from', '>=', fy_start),
                ('date_to', '<=', fy_end),
                ('state', 'in', ['done']),  # only confirmed slips
            ])

            for slip in payslips:
                slip_month = slip.date_from.month  # use payslip start month

                # Find GROSS line in this payslip
                # gross_line = slip.line_ids.filtered(lambda l: l.code == 'GROSS')
                gross_line = slip.line_ids.filtered(lambda l: 'gross' in l.code.lower())
                gross_amount = sum(gross_line.mapped('total'))

                print("MONTH:", slip.date_from, "GROSS:", gross_amount)

                if slip_month in quarters['q1']:
                    record.q1_amount_paid += gross_amount
                elif slip_month in quarters['q2']:
                    record.q2_amount_paid += gross_amount
                elif slip_month in quarters['q3']:
                    record.q3_amount_paid += gross_amount
                elif slip_month in quarters['q4']:
                    record.q4_amount_paid += gross_amount

        record.total_amount_paid = (
            record.q1_amount_paid + record.q2_amount_paid +
            record.q3_amount_paid + record.q4_amount_paid        
        )
    
        record.salary_sec_17_1 = record.total_amount_paid


    @api.depends('total_tax_deducted')
    def _compute_tax_words(self):
        for record in self:
            if record.total_tax_deducted:
                record.total_tax_deducted_words = num2words(record.total_tax_deducted, lang='en_IN').title()
            else:
                record.total_tax_deducted_words = "Zero"

    @api.depends('salary_sec_17_1', 'perquisites_sec_17_2', 'profits_sec_17_3', 'exempt_allowances', 
                 'standard_deduction', 'other_income')
    def _compute_salary_details(self):
        for record in self:
            record.gross_salary_total = (record.salary_sec_17_1 + record.perquisites_sec_17_2 + 
                                        record.profits_sec_17_3)
            record.balance_after_exemptions = record.gross_salary_total - record.exempt_allowances
            record.total_deductions = record.standard_deduction
            record.income_chargeable_salary = record.balance_after_exemptions - record.total_deductions
            record.total_income_before_deductions = record.other_income
            record.gross_total_income = record.income_chargeable_salary + record.other_income

    # @api.depends('epf_employee', 'sec_80ccc', 'sec_80ccd', 'sec_80ccd_1b', 'sec_80ccd_2', 'sec_80ccg',
    #              'sec_80d', 'sec_80e', 'sec_80g', 'sec_80tta', 'other_sec_deductions')
    # def _compute_via_deductions(self):
    #     for record in self:
    #         record.sec_80c_total = record.epf_employee
    #         record.total_chapter_via_deductions = (record.sec_80c_total + record.sec_80ccc + 
    #                                               record.sec_80ccd + record.sec_80ccd_1b + 
    #                                               record.sec_80ccd_2 + record.sec_80ccg + 
    #                                               record.sec_80d + record.sec_80e + record.sec_80g + 
    #                                               record.sec_80tta + record.other_sec_deductions)

    @api.depends('gross_total_income', 'total_chapter_via_deductions', 'credit_87a', 
                 'surcharge', 'relief_sec_89')
    def _compute_tax_calculations(self):
        for record in self:
            record.total_taxable_income = record.gross_total_income - record.total_chapter_via_deductions
            
            # Basic tax calculation (simplified - you may need to implement tax slabs)
            taxable_income = record.total_taxable_income
            if taxable_income <= 250000:
                record.tax_on_total_income = 0
            elif taxable_income <= 500000:
                record.tax_on_total_income = (taxable_income - 250000) * 0.05
            elif taxable_income <= 1000000:
                record.tax_on_total_income = 12500 + (taxable_income - 500000) * 0.20
            else:
                record.tax_on_total_income = 112500 + (taxable_income - 1000000) * 0.30
            
            # Health and Education Cess (4% of tax)
            record.health_education_cess = record.tax_on_total_income * 0.04
            
            record.tax_payable = (record.tax_on_total_income + record.surcharge + 
                                 record.health_education_cess - record.credit_87a)
            record.final_tax_payable = record.tax_payable - record.relief_sec_89


    # add here

    

    # def action_send_form16_email(self):
    #     self.ensure_one()

    #     if not self.employee_id.work_email:
    #         raise UserError("Employee work email is not set!")

    #     mail_values = {
    #         'subject': f'Form 16 - {self.employee_id.name}',
    #         'body_html': f"""
    #             <p>Dear {self.employee_id.name},</p>
    #             <p>Please find your Form 16 details.</p>
    #             <p>
    #                 Assessment Year: {self.assessment_year}<br/>
    #                 Certificate No: {self.certificate_number}
    #             </p>
    #             <p>Regards,<br/>HR Department</p>
    #         """,
    #         'email_to': self.employee_id.work_email,
    #         'email_from': self.env.user.email or '',
    #     }

    #     mail = self.env['mail.mail'].create(mail_values)
    #     mail.send()

    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': 'Success',
    #             'message': 'Form 16 Email Sent Successfully!',
    #             'type': 'success',
    #             'sticky': False,
    #         }
    #     }



    def action_send_form16_email(self):
        self.ensure_one()

        if not self.employee_id.work_email:
            raise UserError("Employee work email is not set!")

        # 🔹 Generate PDF
        report = self.env.ref('hr_employee_form16.action_form16_selvi_format_report')
        pdf_content, _ = report._render_qweb_pdf(self.id)

        attachment = self.env['ir.attachment'].create({
            'name': f'Form16_{self.employee_id.name}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # 🔹 Mail values
        mail_values = {
            'subject': f'Form 16 - {self.employee_id.name}',
            'body_html': f"""
                <p>Dear {self.employee_id.name},</p>
                <p>Please find attached your Form 16.</p>
                <p>
                    Assessment Year: {self.assessment_year}<br/>
                    Certificate No: {self.certificate_number}
                </p>
                <p>Regards,<br/>HR Department</p>
            """,
            'email_to': self.employee_id.work_email,
            'email_from': self.env.user.email or '',
            'attachment_ids': [(4, attachment.id)],
        }

        mail = self.env['mail.mail'].create(mail_values)
        mail.send()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Form 16 Email with PDF Sent Successfully!',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_generate_form16_pdf(self):
        self.ensure_one()

        # Recompute quarterly gross before printing
        self._compute_quarterly_gross()

        return self.env.ref(
            'hr_employee_form16.action_form16_selvi_format_report'
        ).report_action(self)



# class ResCompany(models.Model):
#     _inherit = 'res.company'
    
#     pan_number = fields.Char(string="PAN Number")
#     tan_number = fields.Char(string="TAN Number")