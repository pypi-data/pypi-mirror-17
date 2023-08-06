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
from mastercardmdescustomerservice import *


class SearchTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_example_mdes_search_token_unique_ref(self):
        

        
    
        map = RequestMap()
        map.set("SearchRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        map.set("SearchRequest.AuditInfo.UserId", "A1435477")
        map.set("SearchRequest.AuditInfo.UserName", "John Smith")
        map.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        map.set("SearchRequest.AuditInfo.Phone", "5555551234")
        
        
        response = Search.create(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.AccountPanSuffix", response.get("SearchResponse.Accounts.Account.AccountPanSuffix"),"1234")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.ExpirationDate", response.get("SearchResponse.Accounts.Account.ExpirationDate"),"1215")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.TokenUniqueReference", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenUniqueReference"),"DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.PrimaryAccountNumberUniqueReference", response.get("SearchResponse.Accounts.Account.Tokens.Token.PrimaryAccountNumberUniqueReference"),"FWSPMC0000000004793dac803f190a4dca4bad33c90a11d31")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.TokenSuffix", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenSuffix"),"7639")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.ExpirationDate", response.get("SearchResponse.Accounts.Account.Tokens.Token.ExpirationDate"),"0216")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.DigitizationRequestDateTime", response.get("SearchResponse.Accounts.Account.Tokens.Token.DigitizationRequestDateTime"),"2015-01-20T18:04:35-06:00")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.TokenActivatedDateTime", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenActivatedDateTime"),"2015-01-20T18:04:35-06:00")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.FinalTokenizationDecision", response.get("SearchResponse.Accounts.Account.Tokens.Token.FinalTokenizationDecision"),"A")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.CorrelationId", response.get("SearchResponse.Accounts.Account.Tokens.Token.CorrelationId"),"101234")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.CurrentStatusCode", response.get("SearchResponse.Accounts.Account.Tokens.Token.CurrentStatusCode"),"A")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.CurrentStatusDescription", response.get("SearchResponse.Accounts.Account.Tokens.Token.CurrentStatusDescription"),"Active")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.ProvisioningStatusCode", response.get("SearchResponse.Accounts.Account.Tokens.Token.ProvisioningStatusCode"),"S")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.ProvisioningStatusDescription", response.get("SearchResponse.Accounts.Account.Tokens.Token.ProvisioningStatusDescription"),"Provisioning successful")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.TokenRequestorId", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenRequestorId"),"00212345678")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.WalletId", response.get("SearchResponse.Accounts.Account.Tokens.Token.WalletId"),"103")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.PaymentAppInstanceId", response.get("SearchResponse.Accounts.Account.Tokens.Token.PaymentAppInstanceId"),"92de9357a535b2c21a3566e446f43c532a46b54c46")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.TokenType", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenType"),"S")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.LastCommentId", response.get("SearchResponse.Accounts.Account.Tokens.Token.LastCommentId"),"2376")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceId", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceId"),"3e5edf24a24ba98e27d43e345b532a245e4723d7a9c4f624e93452c92de9357a535b2c21a3566e446f43c532d34s6")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceName", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceName"),"John Phone")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceType", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceType"),"09")
        self.customAssertEqual(ignoreAsserts, "SearchResponse.Accounts.Account.Tokens.Token.Device.SecureElementId", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.SecureElementId"),"92de9357a535b2c21a3566e446f43c532a46b54c46")
        

        BaseTest.putResponse("example_mdes_search_token_unique_ref", response)
        

    
    def test_example_mdes_search_account_pan(self):
        

        
    
        map = RequestMap()
        map.set("SearchRequest.AccountPan", "5412345678901234")
        map.set("SearchRequest.ExcludeDeletedIndicator", "false")
        map.set("SearchRequest.AuditInfo.UserId", "A1435477")
        map.set("SearchRequest.AuditInfo.UserName", "John Smith")
        map.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        map.set("SearchRequest.AuditInfo.Phone", "5555551234")
        
        
        response = Search.create(map)

        ignoreAsserts = []
        
        

        BaseTest.putResponse("example_mdes_search_account_pan", response)
        

    
    def test_example_mdes_search_token(self):
        

        
    
        map = RequestMap()
        map.set("SearchRequest.Token", "5598765432109876")
        map.set("SearchRequest.AuditInfo.UserId", "A14354773")
        map.set("SearchRequest.AuditInfo.UserName", "John Smith")
        map.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        map.set("SearchRequest.AuditInfo.Phone", "5551234658")
        
        
        response = Search.create(map)

        ignoreAsserts = []
        
        

        BaseTest.putResponse("example_mdes_search_token", response)
        

    
    def test_example_mdes_search_comment_id(self):
        

        
    
        map = RequestMap()
        map.set("SearchRequest.CommentId", "123456")
        map.set("SearchRequest.AuditInfo.UserId", "A1435477")
        map.set("SearchRequest.AuditInfo.UserName", "John Smith")
        map.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        map.set("SearchRequest.AuditInfo.PhoneNumber", "5555551234")
        
        
        response = Search.create(map)

        ignoreAsserts = []
        
        

        BaseTest.putResponse("example_mdes_search_comment_id", response)
        

    
    def test_example_mdes_search_payment_app_id(self):
        

        
    
        map = RequestMap()
        map.set("SearchRequest.PaymentAppInstanceId", "645b532a245e4723d7a9c4f62b24f24a24ba98e27d43e34e")
        map.set("SearchRequest.AuditInfo.UserId", "A14354773")
        map.set("SearchRequest.AuditInfo.UserName", "John Smith")
        map.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        map.set("SearchRequest.AuditInfo.Phone", "5551234658")
        
        
        response = Search.create(map)

        ignoreAsserts = []
        
        

        BaseTest.putResponse("example_mdes_search_payment_app_id", response)
        

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

