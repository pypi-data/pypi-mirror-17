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
from mastercardmatch import *


class AddTerminatedMerchantTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_example_add_terminated_merchant(self):
        

        
    
        map = RequestMap()
        map.set("AddMerchantRequest.AcquirerId", "1996")
        map.set("AddMerchantRequest.Merchant.Name", "TEST TECHMERCHANT1")
        map.set("AddMerchantRequest.Merchant.DoingBusinessAsName", "TEST TECHMERCHANT1")
        map.set("AddMerchantRequest.Merchant.MerchantId", "057049905280645")
        map.set("AddMerchantRequest.Merchant.MerchantCategory", "0742")
        map.set("AddMerchantRequest.Merchant.Address.Line1", "6700 Ben Nevis")
        map.set("AddMerchantRequest.Merchant.Address.Line2", "")
        map.set("AddMerchantRequest.Merchant.Address.City", "GLASGOW")
        map.set("AddMerchantRequest.Merchant.Address.Province", "")
        map.set("AddMerchantRequest.Merchant.Address.CountrySubdivision", "MA")
        map.set("AddMerchantRequest.Merchant.Address.PostalCode", "93137")
        map.set("AddMerchantRequest.Merchant.Address.Country", "USA")
        map.set("AddMerchantRequest.Merchant.PhoneNumber", "5675542210")
        map.set("AddMerchantRequest.Merchant.AltPhoneNumber", "5672655441")
        map.set("AddMerchantRequest.Merchant.NationalTaxId", "56733")
        map.set("AddMerchantRequest.Merchant.CountrySubdivisionTaxId", "37354")
        map.set("AddMerchantRequest.Merchant.CATFlag", "N")
        map.set("AddMerchantRequest.Merchant.DateOpened", "04/12/2009")
        map.set("AddMerchantRequest.Merchant.DateClosed", "03/19/2013")
        map.set("AddMerchantRequest.Merchant.ServiceProvLegal", "TEST SVC PRVDER")
        map.set("AddMerchantRequest.Merchant.ServiceProvDBA", "JNL ASSOC")
        map.set("AddMerchantRequest.Merchant.Url[0]", "www.testjj.com")
        map.set("AddMerchantRequest.Merchant.Url[1]", "www.jnltestjj.com")
        map.set("AddMerchantRequest.Merchant.Principal.FirstName", "PAUL")
        map.set("AddMerchantRequest.Merchant.Principal.LastName", "HEMINGHOFF")
        map.set("AddMerchantRequest.Merchant.Principal.MiddleInitial", "L")
        map.set("AddMerchantRequest.Merchant.Principal.Address.Line1", "2200 Shepley Drive")
        map.set("AddMerchantRequest.Merchant.Principal.Address.Line2", "SUITE 789")
        map.set("AddMerchantRequest.Merchant.Principal.Address.City", "BROWNSVILLE")
        map.set("AddMerchantRequest.Merchant.Principal.Address.Province", "")
        map.set("AddMerchantRequest.Merchant.Principal.Address.CountrySubdivision", "MO")
        map.set("AddMerchantRequest.Merchant.Principal.Address.PostalCode", "89022")
        map.set("AddMerchantRequest.Merchant.Principal.Address.Country", "USA")
        map.set("AddMerchantRequest.Merchant.Principal.PhoneNumber", "3906541234")
        map.set("AddMerchantRequest.Merchant.Principal.AltPhoneNumber", "4567390234")
        map.set("AddMerchantRequest.Merchant.Principal.NationalId", "123456789")
        map.set("AddMerchantRequest.Merchant.Principal.DriversLicense.Number", "3K33094")
        map.set("AddMerchantRequest.Merchant.Principal.DriversLicense.CountrySubdivision", "MS")
        map.set("AddMerchantRequest.Merchant.Principal.DriversLicense.Country", "USA")
        map.set("AddMerchantRequest.Merchant.ReasonCode", "04")
        map.set("AddMerchantRequest.Merchant.Comments", "Added for test reasons")
        
        
        response = AddTerminatedMerchant.create(map)

        ignoreAsserts = []
        
        

        BaseTest.putResponse("example_add_terminated_merchant", response)
        

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

