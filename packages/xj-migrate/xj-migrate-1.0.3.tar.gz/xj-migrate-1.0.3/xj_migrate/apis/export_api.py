# encoding: utf-8
"""
@project: djangoModel->export_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 导出AOIView
@created_time: 2022/11/23 18:03
"""

from rest_framework.views import APIView

from main.settings import MEDIA_ROOT
from ..services.doc_export_service import DocExportService
from ..services.excel_export_service import ExcelExport
from ..utils.custom_response import doc_response, excel_response
from ..utils.custom_tool import request_params_wrapper


class exportAPIView(APIView):
    @request_params_wrapper
    def doc_export(self, request_params, *args, **kwargs):
        templet_path = MEDIA_ROOT + "/templet/bxtx_contract_templet.docx"
        data, err = DocExportService.export(request_params, templet_path=templet_path)
        return doc_response(data)

    @request_params_wrapper
    def excel_export(self, request_params, *args, **kwargs):
        templet_path = MEDIA_ROOT + "/templet/test.xls"
        print(templet_path)
        print("request_params", request_params)
        export_instance = ExcelExport(excel_templet_path=templet_path)
        # 写入
        data, err = export_instance.additional_write(input_dict=[request_params])
        # 保存
        excel_data, err = export_instance.save(workbook=export_instance.additional_write_wb)
        return excel_response(excel_data)
