/*
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "settings_music.h"
#include "settings_menu.h"
#include "settings_window.h"

#include "applib/ui/ui.h"
#include "kernel/pbl_malloc.h"
#include "services/common/i18n/i18n.h"

typedef struct SettingsMusicData {
  SettingsCallbacks callbacks;
} SettingsMusicData;

static void prv_draw_row_cb(SettingsCallbacks *context, GContext *ctx, const Layer *cell_layer,
                            uint16_t row, bool selected) {
  menu_cell_basic_draw(ctx, cell_layer, "Placeholder", NULL, NULL);
}

static uint16_t prv_num_rows_cb(SettingsCallbacks *context) {
  return 1;
}

static void prv_select_click_cb(SettingsCallbacks *context, uint16_t row) {
  // Do nothing for now
}

static Window *prv_init(void) {
  SettingsMusicData *data = app_malloc_check(sizeof(*data));
  *data = (SettingsMusicData){};

  data->callbacks = (SettingsCallbacks){
      .draw_row = prv_draw_row_cb,
      .num_rows = prv_num_rows_cb,
      .select_click = prv_select_click_cb,
  };

  return settings_window_create(SettingsMenuItemMusic, &data->callbacks);
}

const SettingsModuleMetadata *settings_music_get_info(void) {
  static const SettingsModuleMetadata s_module_info = {
      .name = i18n_noop("Music Settings"),
      .init = prv_init,
  };

  return &s_module_info;
}
