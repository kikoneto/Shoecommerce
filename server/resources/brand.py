from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from managers.brand import BrandManager
from models import RoleType
from models.products import *
from schemas.request.brand import CreateBrandRequestSchema
from schemas.response.brand import CreateBrandResponseSchema, BrandNameOnlyResponseSchema
from utils.decorators import validate_schema, token_required, permission_required

from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

config = cloudinary.config(secure=True)


class Brand(Resource):
    @validate_schema(CreateBrandRequestSchema)
    @permission_required(RoleType.admin)
    def post(self):
        # uploaded_files = request.files.get('file', '')
        # print(uploaded_files)
        # a = request
        # print(a)
        #
        # upload_result = cloudinary.uploader.upload(uploaded_files)

        # return jsonify(upload_result)

        brand = BrandManager.create(request.get_json())
        schema = CreateBrandResponseSchema()
        return schema.dumps(brand)

    def get(self):
        brand_name = request.args.get("brand")
        schema = CreateBrandResponseSchema()
        if not brand_name:
            brands = BrandManager.get_all()
            brand_name_schema = BrandNameOnlyResponseSchema()
            return brand_name_schema.dump(brands, many = True)

        if brand_name == "all":
            brands = BrandManager.get_all()
            return schema.dumps(brands, many=True)

        elif brand_name:
            brands = BrandManager.get_by_name(brand_name)
            return schema.dumps(brands)

        raise BadRequest("You should use query parameters, check the documentation!")

        # TODO
        # Implement Delete func
