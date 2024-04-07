import re
from abc import ABC, abstractmethod
from typing import List
import numpy.typing as npt
import simplelpr


class CarScraper(ABC):
    @property
    @abstractmethod
    def cars(self):
        pass

    @abstractmethod
    def scrape(self):
        pass

    def numberplate_detector(self, image):
        try:
            setup_p = simplelpr.EngineSetupParms()
            eng = simplelpr.SimpleLPR(setup_p)
            eng.set_countryWeight(90, 1)
            eng.realizeCountryWeights()

            proc = eng.createProcessor()

            # Enable the plate region detection and crop to plate region features.
            proc.plateRegionDetectionEnabled = True
            proc.cropToPlateRegionEnabled = True
            cds = proc.analyze(image)
            plates = [cm.text.replace(" ", "") for cand in cds for cm in cand.matches]

            if plates:
                return self.fix_number_plate(plates[0])
            else:
                return ""
        except Exception as err:
            print("Error in number plate detector", err)
            return ""

    def get_numberplate(self, images: List[npt.NDArray]) -> List[str]:
        number_plates = []
        for image in images:
            plate = self.numberplate_detector(image)
            if plate:
                number_plates.append(plate)
        return number_plates

    @abstractmethod
    def get_image_sources(self, page_element) -> List[npt.NDArray]:
        pass

    @staticmethod
    def fix_number_plate(number_plate) -> str:
        number_plate = number_plate.replace(" ", "").upper()
        pattern = r'^([A-Z]{2})([A-Z]|[0-9])([A-Z]|[0-9])([A-Z]{3})$'
        # Check if the number plate matches the pattern
        match = re.match(pattern, number_plate)
        if match:
            groups = list(match.groups())
            for i in [1, 2]:  # Indexes for the 2nd and 3rd characters
                if groups[i] == "I":
                    groups[i] = "1"
                elif groups[i] == "O":
                    groups[i] = "0"
            fixed_number_plate = "".join(groups).upper()
        else:
            fixed_number_plate = ""

        return fixed_number_plate

    @staticmethod
    def is_valid_uk_number_plate(plate) -> bool:
        pattern = r'^[A-Z]{2}\d{2}\s?[A-Z]{3}$'

        return bool(re.match(pattern, plate))
