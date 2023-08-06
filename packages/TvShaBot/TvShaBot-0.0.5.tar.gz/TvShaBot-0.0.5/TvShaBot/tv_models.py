from pydantic import BaseModel


class CountryModel(BaseModel):
    name: str


class NetworkModel(BaseModel):
    name: str
    country: CountryModel


class TVShow(BaseModel):
    name: str
    network: NetworkModel
    summary: str

    def info(self):
        name = self.name
        net_name = self.network.name
        country = self.network.country.name
        summary = self.summary

        show_info = [
            f"Name: {name}",
            f"Network Name: {net_name}",
            f"Network Country Name: {country}",
            f"Summary: {summary}",
        ]

        return show_info
