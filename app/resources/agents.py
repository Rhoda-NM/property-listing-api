from flask import request
from flask_restx import Namespace, Resource
from sqlalchemy import or_

from ..models.user import User
from ..schemas.user import UserSchema
from ..schemas.listing import ListingSchema

# 🔹 RESTX Namespace
agents_ns = Namespace("agents", description="Agents & profiles")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
listings_schema = ListingSchema(many=True)


@agents_ns.route("")
class AgentList(Resource):
    def get(self):
        """
        List agents (with optional search)
        ---
        Query params:
        - q: search string (name, email, company)
        - page: page number
        - per_page: items per page
        """
        q = User.query.filter_by(is_agent=True)
        args = request.args

        search = args.get("q")
        if search:
            pattern = f"%{search}%"
            q = q.filter(
                or_(
                    User.name.ilike(pattern),
                    User.email.ilike(pattern),
                    User.company.ilike(pattern),
                )
            )

        page = int(args.get("page", 1))
        per_page = min(int(args.get("per_page", 20)), 100)

        paged = q.paginate(page=page, per_page=per_page, error_out=False)

        items = []
        for agent in paged.items:
            data = user_schema.dump(agent)
            data["listing_count"] = len(agent.listings or [])
            items.append(data)

        return {
            "items": items,
            "total": paged.total,
            "page": page,
            "per_page": per_page,
        }


@agents_ns.route("/<int:agent_id>")
class AgentDetail(Resource):
    def get(self, agent_id: int):
        """Get agent profile plus their listings"""
        agent = User.query.filter_by(id=agent_id, is_agent=True).first()
        if not agent:
            return {"message": "Agent not found"}, 404

        agent_data = user_schema.dump(agent)
        listings_data = listings_schema.dump(agent.listings or [])
        return {"agent": agent_data, "listings": listings_data}

    