#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

import unittest
import time
from mastercardapicore import RequestMap
from base_test import BaseTest
from mastercardlocations import *


class MerchantLocationsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_merchants(self):
        

        
    
        map = RequestMap()
        map.set("Details", "acceptance.paypass")
        map.set("PageOffset", "0")
        map.set("PageLength", "5")
        map.set("Latitude", "38.53463")
        map.set("Longitude", "-90.286781")
        
        
        response = MerchantLocations.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "Merchants.PageOffset", response.get("Merchants.PageOffset"),"0")
        self.customAssertEqual(ignoreAsserts, "Merchants.TotalCount", response.get("Merchants.TotalCount"),"3")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Id", response.get("Merchants.Merchant[0].Id"),"36564")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Name", response.get("Merchants.Merchant[0].Name"),"Merchant 36564")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Category", response.get("Merchants.Merchant[0].Category"),"7 - Dry Cleaners And Laundry Services")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Name", response.get("Merchants.Merchant[0].Location.Name"),"Merchant 36564")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Distance", response.get("Merchants.Merchant[0].Location.Distance"),"0.9320591049747101")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.DistanceUnit", response.get("Merchants.Merchant[0].Location.DistanceUnit"),"MILE")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.Line1", response.get("Merchants.Merchant[0].Location.Address.Line1"),"3822 West Fork Street")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.City", response.get("Merchants.Merchant[0].Location.Address.City"),"Great Falls")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.PostalCode", response.get("Merchants.Merchant[0].Location.Address.PostalCode"),"51765")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.CountrySubdivision.Name", response.get("Merchants.Merchant[0].Location.Address.CountrySubdivision.Name"),"Country Subdivision 517521")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.CountrySubdivision.Code", response.get("Merchants.Merchant[0].Location.Address.CountrySubdivision.Code"),"Country Subdivision Code 517521")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.Country.Name", response.get("Merchants.Merchant[0].Location.Address.Country.Name"),"Country 5175215")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Address.Country.Code", response.get("Merchants.Merchant[0].Location.Address.Country.Code"),"Country Code 5175215")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Point.Latitude", response.get("Merchants.Merchant[0].Location.Point.Latitude"),"38.52114017591121")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Location.Point.Longitude", response.get("Merchants.Merchant[0].Location.Point.Longitude"),"-90.28678100000002")
        self.customAssertEqual(ignoreAsserts, "Merchants.Merchant[0].Acceptance.PayPass.Register", response.get("Merchants.Merchant[0].Acceptance.PayPass.Register"),"true")
        

        BaseTest.putResponse("example_merchants", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

