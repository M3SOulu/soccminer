/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package ms.appcenter.sampleapp.android;

import android.content.Context;

import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;

import org.junit.Rule;
import org.junit.After;
import com.microsoft.appcenter.espresso.Factory;
import com.microsoft.appcenter.espresso.ReportHelper;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.assertEquals;

/**
 * Instrumentation test, which will execute on an Android device.
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedTest {
    // Mandatory dependency
    static {
        System.loadLibrary("SasquatchBreakpad");
    }

    @Rule
    public ReportHelper reportHelper = Factory.getReportHelper();

    @After
    public void TearDown() {
        reportHelper.label("Stopping App");
    }

    private interface HasEnabled {
    // Validator
    boolean isEnabled();
    // Enabler
    void setEnabled(boolean enabled);
    }

    @Test
    public void useAppContext() {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getInstrumentation().getTargetContext();

        assertEquals("ms.appcenter.sampleapp.android", appContext.getPackageName());
    }

    // Update type
    private enum UpdateTrackEnum {
    PUBLIC(UpdateTrack.PUBLIC, R.string.appcenter_distribute_track_public_enabled), PRIVATE(UpdateTrack.PRIVATE, R.string.appcenter_distribute_track_private_enabled);

    public final int value;

    @StringRes
    public final int summaryRes;

    UpdateTrackEnum(int value, @StringRes int summaryRes) {
    	this.value = value;
        this.summaryRes = summaryRes;
    }

    static UpdateTrackEnum init(int value) {
        for (UpdateTrackEnum updateTrackEnum : UpdateTrackEnum.values()) {
            if (updateTrackEnum.value == value) {
                return updateTrackEnum;
            }
        }
        return PUBLIC;
    }
  } //End of Enumerator
}






